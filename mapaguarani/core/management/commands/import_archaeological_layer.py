from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from core.models import ArchaeologicalPlace, MapLayer, EthnicGroup, GuaraniPresence, Population

import utm
import csv


class Command(BaseCommand):
    help = 'Import village layer'

    def add_arguments(self, parser):
        parser.add_argument('shapefile_path', nargs='+', type=str)

    def handle(self, *args, **options):

        csv_path = options['shapefile_path'][0]

        with open(csv_path, newline='') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter='|', quotechar='"')
            for row in spamreader:
                archaeological_layer, _ = MapLayer.objects.get_or_create(name=row.get('camada'))
                archaeological_layer.save()

                kwargs = {
                    'layer': archaeological_layer,
                    'name': row['nome_sitio'],
                    'cnsa': row['cnsa'],
                    'acronym': row['sigla'],
                    'biblio_references': row['fonte'],
                    'institution': row['instituições'],

                    'hydrography': row['hidrografia'],
                    'phase': row['fase'],
                    'dating': row['datacao'],
                    'deviation': row['desvio'],
                    'chrono_ref': row['ref_cronologica'],
                    'ap_date': row['data_ap'],
                    'calibrated_dating': row['datacao_calibrada'],
                    'dating_method': row['metodo_datacao'],
                    'lab_code': row['codigo_lab'],
                }

                archaeological_place = ArchaeologicalPlace(**kwargs)

                if row['precisao'] == 'prov':
                    archaeological_place.position_precision = 'by_city'
                elif row['precisao'] == 'biblio':
                    archaeological_place.position_precision = 'exact'
                elif row['precisao'] == 'aprox':
                    archaeological_place.position_precision = 'approximate'

                coords = row['coords'].split()

                try:
                    latitude, longitude = utm.to_latlon(int(coords[1]), int(coords[2]), int(coords[0][0:2]), coords[0][-1])
                except:
                    import pdb;pdb.set_trace()

                archaeological_place.status = 'public'

                archaeological_place.geometry = Point(longitude, latitude)
                archaeological_place.save()

        self.stdout.write('\n')
        self.stdout.write(
            'Camada de sítios arqueológicos importada com sucesso! Caminho do arquivo fornecido: "%s"' % csv_path)
        self.stdout.write('\n')
