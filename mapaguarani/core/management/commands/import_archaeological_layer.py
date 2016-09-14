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

        archaeological_layer, _ = MapLayer.objects.get_or_create(name='Sítios Arqueológicos')
        archaeological_layer.description = 'Camada de Sítios Arqueológicos'
        archaeological_layer.save()

        with open(csv_path, newline='') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter='|', quotechar='"')
            for row in spamreader:

                kwargs = {
                    'layer': archaeological_layer,
                    'name': row['nome_sitio'],
                    'cnsa': row['cnsa'],
                    'code': row['cod_sitio'],
                    'acronym': row['sigla'],
                    'biblio_references': row['Fonte'],
                }

                archaeological_place = ArchaeologicalPlace(**kwargs)

                # if row['aprox']:
                #     archaeological_place.position_precision = 'by_city'
                # else:
                #     archaeological_place.position_precision = 'exact'

                # import ipdb;ipdb.set_trace()
                coords = row['coords'].split()

                try:
                    latitude, longitude = utm.to_latlon(int(coords[1]), int(coords[2]), int(coords[0][0:2]), coords[0][-1])
                except:
                    import ipdb;ipdb.set_trace()

                archaeological_place.geometry = Point(longitude, latitude)
                archaeological_place.save()

        self.stdout.write('\n')
        self.stdout.write(
            'Camada de sítios arqueológicos importada com sucesso! Caminho do arquivo fornecido: "%s"' % csv_path)
        self.stdout.write('\n')
