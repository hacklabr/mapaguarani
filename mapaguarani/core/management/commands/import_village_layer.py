from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.utils import LayerMapping
from core.models import IndigenousVillage

class Command(BaseCommand):
    help = 'Import village layer'
    villages_mapping = {
        'name': 'ALDEIA_GUA',
        'other_names': 'OUTRAS_DEN',
        'ethnic_groups2': 'GRUPO_ETNI',
        'population': 'POPULACAO_',
        'guarani_presence': 'PRESENCA_G',
        'prominent_subgroup': 'SUB_GRUPO_',
        'position': 'POINT',
    }

    def add_arguments(self, parser):
        parser.add_argument('shapefile_path', nargs='+', type=str)

    def handle(self, *args, **options):
        # with options['shapefile_path'] as shapefile_path:
        # import ipdb; ipdb.set_trace()
        shapefile_path = options['shapefile_path'][0]

        lm = LayerMapping(IndigenousVillage, shapefile_path, self.villages_mapping)
        lm.save(verbose=True)

        self.stdout.write('Camada de aldeias importada com sucesso! Caminho: "%s"' % shapefile_path)
