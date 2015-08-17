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

        def _get_ethnic_group(group):
            ethnic_group, _ = EthnicGroup.objects.get_or_create(name=group)
            return ethnic_group

        def _get_ethnic_subgroup(group):
            ethnic_group, _ = ProminentEthnicSubGroup.objects.get_or_create(name=group)
            return ethnic_group

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

                # 'land_tenure': feat.get('SITUACAO_F'),
                # 'land_tenure_status': feat.get('STATUS_REV'),
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

            for group in feat.get('SUBGRUPO_P').split(','):
                indigenous_land.prominent_subgroup.add(_get_ethnic_subgroup(group))

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
