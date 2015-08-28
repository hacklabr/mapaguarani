from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.utils import LayerMapping
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

        villages_layer, _ = MapLayer.objects.get_or_create(name='Aldeias Indígenas')
        villages_layer.description = 'Camada de Aldeias Indígenas dos povos Guarani'
        villages_layer.save()

        def _get_ethnic_group(groups):

            groups_names = []
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
            group_list = groups.split()
            if len(group_list) == 1:
                if '/' not in group_list[0]:
                    groups_names.append(group_list[0])
                else:
                    group_list = groups.split('/')
                    if len(group_list) == 2:
                        groups_names.append(group_list[0])
                        groups_names.append(group_list[1])
            elif '/' in groups:
                if group_list and len(group_list) == 3:
                    groups_names.append(group_list[0])
                    if '/' in group_list[2]:
                        group_list2 = group_list[2].split('/')
                        groups_names.append(group_list2[0])
                        groups_names.append(group_list2[1])
                    else:
                        groups_names.append(group_list[2])
                else:
                    for group in group_list:
                        if not '/' in group:
                            groups_names.append(group)
                        else:
                            if len(group) > 1:
                                groups_names.append(group.split('/')[1])
            else:
                print(group_list)

            for group_name in groups_names:
                try:
                    yield ProminentEthnicSubGroup.objects.get(name=group_name)
                except ProminentEthnicSubGroup.DoesNotExist:
                    print('Não achou: ' + group_name)
                    print(groups)
                    print('\n')

        for feat in source_layer:
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

            indigenous_village.position = feat.geom.wkt

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
