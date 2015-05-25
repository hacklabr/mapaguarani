from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import fromstr, MultiPolygon
from core.models import IndigenousLand, MapLayer, EthnicGroup


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

                'land_tenure': feat.get('SITUACAO_F'),
                'land_tenure_status': feat.get('STATUS_REV'),
                'associated_land': feat.get('TERRAS_ASS'),
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
                print('Terra indígena: ' + indigenous_land.name + 'Posição convertida de Polígono para Multipolígono.')

            for group in feat.get('SUBGRUPO_P').split(','):
                indigenous_land.prominent_subgroup.add(_get_ethnic_group(group))
            indigenous_land.save()

        self.stdout.write('Camada de terras indígenas importada com sucesso! Caminho do arquivo fornecido: "%s"' % shapefile_path)
