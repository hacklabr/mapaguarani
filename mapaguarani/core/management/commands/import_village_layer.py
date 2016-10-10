from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from core.models import IndigenousVillage, MapLayer, EthnicGroup, GuaraniPresence, Population, ProminentEthnicSubGroup

import datetime


class Command(BaseCommand):
    help = 'Import village layer'

    def add_arguments(self, parser):
        parser.add_argument('shapefile_path', nargs='+', type=str)

    def handle(self, *args, **options):

        shapefile_path = options['shapefile_path'][0]
        ds = DataSource(shapefile_path)
        source_layer = ds[0]

        def _get_ethnic_group(groups):

            groups_names = groups.split(',')

            for group_name in groups_names:
                group_name = group_name.strip()
                if group_name:
                    group, created = EthnicGroup.objects.get_or_create(name=group_name)
                    if created:
                        print('Criado grupo etnico: ' + group_name)
                    yield group

        def _get_ethnic_subgroup(groups):
            groups_names = groups.split(',')

            for group_name in groups_names:
                group_name = group_name.strip()
                if group_name:
                    group, created = ProminentEthnicSubGroup.objects.get_or_create(name=group_name)
                    if created:
                        print('Criado subgrupo etnico: ' + group_name)
                    yield group

        for feat in source_layer:

            villages_layer, _ = MapLayer.objects.get_or_create(name=feat.get('CAMADA'))
            villages_layer.save()

            kwargs = {
                'layer': villages_layer,
                'name': feat.get('ALDEIA_GUA'),
                'other_names': feat.get('OUTRAS_DEN'),
                'position_source': feat.get('FONTE_LOCA'),
                'private_comments': feat.get('OBSERVACOE'),
                'public_comments': feat.get('OBSERVACO2'),
            }

            indigenous_village = IndigenousVillage(**kwargs)

            position_precision = feat.get('PRECISAO_D')
            if position_precision == 'Exata' or position_precision == 'Exato':
                indigenous_village.position_precision = 'exact'
            elif position_precision == 'Aproximada':
                indigenous_village.position_precision = 'approximate'
            elif not position_precision:
                indigenous_village.position_precision = 'no_info'
            else:
                self.stdout.write('Precisão da posição não encontrata: ' + position_precision)

            indigenous_village.geometry = feat.geom.wkt

            try:
                # try to save as MultPolygon
                indigenous_village.save()
            except:
                self.stdout.write('Falha ao salvar aldeia indígena\n')

            ethnic_groups = _get_ethnic_group(feat.get('GRUPO_ETNI'))
            for group in ethnic_groups:
                indigenous_village.ethnic_groups.add(group)

            ethnic_subgroups = _get_ethnic_subgroup(feat.get('SUB_GRUPO_'))
            for ethnic_subgroup in ethnic_subgroups:
                indigenous_village.prominent_subgroup.add(ethnic_subgroup)

            guarani_presence = feat.get('PRESENCA_G')
            if guarani_presence == 'Sim':
                # FIXME ver questão da fonte.
                guarani_presence = GuaraniPresence(
                    presence=True, date=datetime.date(2015, 1, 1), source='CTI', village=indigenous_village)
                guarani_presence.save()
            elif guarani_presence == 'Não':
                pass
            else:
                self.stdout.write('Falha ao ler Presença Guarani. Valor: ' + guarani_presence)

            population = feat.get('POPULACAO_')
            if population:
                try:
                    population = int(population.split()[0])
                    population = Population(
                        population=population,
                        date=datetime.date(2013, 1, 1),
                        source=feat.get('FONTE_POPU'),
                        village=indigenous_village
                    )
                    population.save()
                except:
                    self.stdout.write('Falha ao ler população. População: ' + population)

            indigenous_village.save()

        self.stdout.write('\n')
        self.stdout.write(
            'Camada de aldeias importada com sucesso! Caminho do arquivo fornecido: "%s"' % shapefile_path)
        self.stdout.write('\n')
