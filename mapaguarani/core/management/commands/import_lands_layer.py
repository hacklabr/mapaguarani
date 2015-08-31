from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import fromstr, MultiPolygon
from core.models import IndigenousLand, MapLayer, EthnicGroup, ProminentEthnicSubGroup, LandTenure, LandTenureStatus


class Command(BaseCommand):
    help = 'Import village layer'

    def add_arguments(self, parser):
        parser.add_argument('shapefile_path', nargs='+', type=str)

    def handle(self, *args, **options):
        shapefile_path = options['shapefile_path'][0]
        ds = DataSource(shapefile_path)
        source_layer = ds[0]

        lands_layer, _ = MapLayer.objects.get_or_create(name='Terras Indígenas')
        lands_layer.description = 'Camada de Terras Indígenas dos povos Guarani'
        lands_layer.save()

        def _get_ethnic_group(groups):

            groups_names = []
            if ',' in groups:
                group_list = groups.split(',')
            else:
                group_list = groups.split()
            if len(group_list) == 1:
                groups_names.append(group_list[0])
            elif 'e' in group_list and len(group_list) == 3:
                groups_names.append(group_list[0])
                groups_names.append(group_list[2])
            elif len(group_list) == 4:
                groups_names.append(group_list[0][:-1])
                groups_names.append(group_list[1])
                groups_names.append(group_list[3])
            elif len(group_list) == 2 or len(group_list) == 3:
                groups_names = group_list
            else:
                print('EthnicGroup:')
                print(group_list)

            for group_name in groups_names:
                try:
                    yield EthnicGroup.objects.get(name=group_name)
                except EthnicGroup.DoesNotExist:
                    print('Não achou EthnicGroup: ' + group_name)

        def _get_ethnic_subgroup(groups):
            groups_names = []
            if ',' in groups:
                group_list = groups.split(',')
            else:
                group_list = groups.split()
            if len(group_list) == 1:
                if '/' not in group_list[0]:
                    groups_names.append(group_list[0])
                else:
                    group_list = groups.split('/')
                    if len(group_list) == 2:
                        groups_names = group_list
            elif '/' in groups:
                if group_list and len(group_list) == 3:
                    groups_names.append(group_list[0])
                    if '/' in group_list[2]:
                        group_list2 = group_list[2].split('/')
                        groups_names.append(group_list2[0])
                        groups_names.append(group_list2[1])
                    else:
                        groups_names.append(group_list[2])
                elif len(group_list) == 2:
                    groups_names.append(group_list[0])
                    if '/'in group_list[1]:
                        groups_names.append(group_list[1][1:])
                    else:
                        groups_names.append(group_list[1])
                elif len(group_list) == 4:
                    groups_names.append(group_list[0])
                    groups_names.append(group_list[2])
                    if '/'in group_list[3]:
                        groups_names.append(group_list[3][1:])
                    else:
                        groups_names.append(group_list[3])
            elif len(group_list) == 2 or len(group_list) == 3:
                groups_names = group_list
            else:
                print(group_list)

            for group_name in groups_names:
                try:
                    yield ProminentEthnicSubGroup.objects.get(name=group_name)
                except ProminentEthnicSubGroup.DoesNotExist:
                    print('Não achou: ' + group_name)
                    print(groups)
                    print('\n')

        def _get_land_tenure(name):
            land_tenure, _ = LandTenure.objects.get_or_create(name=name)
            return land_tenure

        def _get_land_tenure_status(name):
            land_tenure_status, _ = LandTenureStatus.objects.get_or_create(name=name)
            return land_tenure_status

        for feat in source_layer:

            official_area = feat.get('AREA').replace(".", "").replace(",", ".")
            if official_area:
                official_area = float(official_area)
            else:
                official_area = 0.0

            kwargs = {
                'layer': lands_layer,
                'name': feat.get('TERRA_INDI'),
                'other_names': feat.get('OUTRAS_DEN'),
                'official_area': official_area,
                'claim': feat.get('REIVINDICA'),
                'demand': feat.get('DEMANDA'),
                'source': feat.get('FONTE'),
                'private_comments': feat.get('OBS_PRIVAD'),
                'public_comments': feat.get('OBS_PUBLIC'),
                'guarani_exclusive_possession_area_portion': float(feat.get('PORCAO_ARE')),
                'others_exclusive_possession_area_portion': float(feat.get('PORCAO_AR2')),

                # 'associated_land': feat.get('TERRAS_ASS'),
            }

            indigenous_land = IndigenousLand(**kwargs)
            indigenous_land.polygon = feat.geom.wkt

            try:
                # try to save as MultPolygon
                indigenous_land.save()
            except:
                # Convert polygon to MultPolgon before save
                poly = fromstr(feat.geom.wkt)
                multi_poly = MultiPolygon(poly)
                indigenous_land.polygon = multi_poly.wkt
                indigenous_land.save()
                # self.stdout.write('Terra indígena: ' + indigenous_land.name + 'Posição convertida de Polígono para Multipolígono.')

            ethnic_groups = _get_ethnic_group(feat.get('GRUPO_ETNI'))
            for group in ethnic_groups:
                indigenous_land.ethnic_groups.add(group)

            ethnic_subgroups = _get_ethnic_subgroup(feat.get('SUBGRUPO_P'))
            for ethnic_subgroup in ethnic_subgroups:
                indigenous_land.prominent_subgroup.add(ethnic_subgroup)

            land_tenure = feat.get('SITUACAO_F')
            if land_tenure == 'Sem Providências':
                indigenous_land.land_tenure = _get_land_tenure('Sem Providências')
            elif land_tenure in ['Regularizada', 'Regularizada (Em revisão de limites)']:
                indigenous_land.land_tenure = _get_land_tenure('Regularizada')
            elif land_tenure in ['Desapropriada', 'Desapropriada (Reivindicação de Identificação)']:
                indigenous_land.land_tenure = _get_land_tenure('Desapropriada')
            elif land_tenure in ['Em processo de desapropriação', 'Em processo de despropriação pelo Estado.',
                                 'Área em processo de despropriação pelo Estado.', 'Em processo de Desapropriação.',
                                 'Em processo de Desapropriação']:
                indigenous_land.land_tenure = _get_land_tenure('Em processo de desapropriação')
            elif land_tenure == 'Delimitada':
                indigenous_land.land_tenure = _get_land_tenure('Delimitada')
            elif land_tenure == 'Em estudo':
                indigenous_land.land_tenure = _get_land_tenure('Em estudo')
            elif land_tenure == 'Declarada':
                indigenous_land.land_tenure = _get_land_tenure('Declarada')
            elif land_tenure in ['Adquirida', 'Dominial Indígena']:
                indigenous_land.land_tenure = _get_land_tenure('Adquirida')
            elif land_tenure == 'Homologada':
                indigenous_land.land_tenure = _get_land_tenure('Homologada')
            else:
                self.stdout.write('Situação fundiária não encontrata! NOME: ' + feat.get('TERRA_INDI') + 'STATUS: ' + land_tenure)

            land_tenure_status = feat.get('STATUS_REV')
            if land_tenure_status == 'Sem Revisão':
                indigenous_land.land_tenure_status = _get_land_tenure_status('Sem Revisão')
            elif land_tenure_status == 'Não Delimitada':
                indigenous_land.land_tenure_status = _get_land_tenure_status('Não Delimitada')
            elif land_tenure_status == 'Terra Revisada':
                indigenous_land.land_tenure_status = _get_land_tenure_status('Terra Revisada')
            elif land_tenure_status == 'Terra Original':
                indigenous_land.land_tenure_status = _get_land_tenure_status('Terra Original')
            else:
                self.stdout.write('Status de revisão fundiária não encontrata: ' + land_tenure_status)

            indigenous_land.save()

        self.stdout.write('Camada de terras indígenas importada com sucesso! Caminho do arquivo fornecido: "%s"' % shapefile_path)
