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

        lands_layer, _ = MapLayer.objects.get_or_create(name='Terras Indígenas - Povos não Guaranis')
        lands_layer.description = 'Camada de Terras Indígenas'
        lands_layer.save()

        def _get_ethnic_group(groups, create=False):
            """
            The ethnic groups names must be separated by coma
            """
            groups_names = []

            for group_name in groups.split(','):
                group_name = group_name.strip()
                if not group_name:
                    return
                if create:
                    ethnic_group, created = EthnicGroup.objects.get_or_create(name=group_name)
                    if created:
                        self.stdout.write('O povo {0} foi criado.'.format(group_name))
                    yield ethnic_group
                else:
                    try:
                        yield EthnicGroup.objects.get(name=group_name)
                    except EthnicGroup.DoesNotExist:
                        self.stdout.write('O povo {0} não foi encontrato e não será criado, por favor verifique o arquivo de importação.'.format(group_name))


        def _get_ethnic_subgroup(groups, create=False):
            """
            The ethnic subgroups names must be separated by coma
            """
            for group_name in groups.split(','):
                group_name = group_name.strip()
                if create:
                    ethnic_subgroup, _ = ProminentEthnicSubGroup.objects.get_or_create(name=group_name)
                    yield ethnic_subgroup
                else:
                    try:
                        yield EthnicGroup.objects.get(name=group_name)
                    except ProminentEthnicSubGroup.DoesNotExist:
                        self.stdout.write('O subgrupo Guarani {0} não foi encontrato e não será criado, por favor verifique o arquivo de importação.'.format(group_name))

        for feat in source_layer:

            official_area = feat.get('AREA')
            if isinstance(official_area, str):
                official_area.replace(".", "").replace(",", ".")
                official_area = float(official_area)
            if not official_area:
                official_area = 0.0

            kwargs = {
                'layer': lands_layer,
                'name': feat.get('TERRA_INDI'),
                # 'other_names': feat.get('OUTRAS_DEN'),
                'official_area': official_area,
                # 'claim': feat.get('REIVINDICA'),
                # 'demand': feat.get('DEMANDA'),
                'source': feat.get('FONTE'),
                # 'private_comments': feat.get('OBS_PRIVAD'),
                # 'public_comments': feat.get('OBS_PUBLIC'),
                # 'guarani_exclusive_possession_area_portion': float(feat.get('PORCAO_ARE')),
                # 'others_exclusive_possession_area_portion': float(feat.get('PORCAO_AR2')),
                # 'associated_land': feat.get('TERRAS_ASS'),
            }

            indigenous_land = IndigenousLand(**kwargs)

            land_tenure = feat.get('SITUACAO_F')
            if land_tenure == 'Em Estudo':
                land_tenure ='Em estudo'
            if not LandTenure.objects.filter(name=land_tenure).exists():
                raise(BaseException('Situação fundiária não encontrata! NOME: {0} STATUS: {1}'.format(feat.get('TERRA_INDI'), land_tenure)))
            indigenous_land.land_tenure = LandTenure.objects.get(name=land_tenure)

            land_tenure_status = feat.get('STATUS_REV')
            if not LandTenureStatus.objects.filter(name=land_tenure_status).exists():
                raise(BaseException('Status de revisão fundiária não encontrata: {}'.format(land_tenure_status)))
            indigenous_land.land_tenure_status = LandTenureStatus.objects.get(name=land_tenure_status)

            indigenous_land.geometry = feat.geom.wkt
            try:
                # try to save as MultPolygon
                indigenous_land.save()
            except:
                # Convert polygon to MultPolgon before save
                poly = fromstr(feat.geom.wkt)
                multi_poly = MultiPolygon(poly)
                indigenous_land.geometry = multi_poly.wkt
                indigenous_land.save()
                # self.stdout.write('Terra indígena: ' + indigenous_land.name + 'Posição convertida de Polígono para Multipolígono.')

            ethnic_groups = _get_ethnic_group(feat.get('GRUPO_ETNI'), create=True)
            for group in ethnic_groups:
                indigenous_land.ethnic_groups.add(group)

            # ethnic_subgroups = _get_ethnic_subgroup(feat.get('SUBGRUPO_P'))
            # for ethnic_subgroup in ethnic_subgroups:
            #     indigenous_land.prominent_subgroup.add(ethnic_subgroup)

            indigenous_land.save()

        self.stdout.write('Camada de terras indígenas importada com sucesso! Caminho do arquivo fornecido: "%s"' % shapefile_path)
