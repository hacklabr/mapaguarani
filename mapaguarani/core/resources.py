from import_export import fields, resources
from core.models import IndigenousLand
from django.utils.translation import ugettext_lazy as _

from boundaries.models import City


class IndigenousVillageResource(resources.ModelResource):
    guarani_presence = fields.Field()
    cities = fields.Field()
    states = fields.Field()

    class Meta:
        model = IndigenousLand

        fields = ('name', 'other_names', 'ethnic_groups', 'prominent_subgroup',
                  'official_area', 'land_tenure', 'documents', 'cities', 'states',)

        export_order = ('name', 'other_names', 'ethnic_groups', 'prominent_subgroup',
                        'guarani_presence', 'official_area', 'land_tenure', 'documents',
                        'cities', 'states',)

    def get_export_headers(self):
        return [
            'Terra Indígena TI - (Aldeias Guarani)',
            'Outras denominações da TI',
            'Grupo(s) étnico(s)',
            'Subgrupo proeminente',
            'Presença Guarani',
            'Área da TI (ha)',
            'Situação Jurídica',
            'Documentação',
            'Município',
            'UF',
        ]

    def dehydrate_ethnic_groups(self, obj):
        return '; '.join(obj.ethnic_groups.values_list('name', flat=True))

    def dehydrate_prominent_subgroup(self, obj):
        return '; '.join(obj.prominent_subgroup.values_list('name', flat=True))

    def dehydrate_guarani_presence(self, obj):
        return _('Yes') if obj.population > 0 else _('No')

    def dehydrate_land_tenure(self, obj):
        return obj.land_tenure.name if obj.land_tenure else ''

    def dehydrate_documents(self, obj):
        return '; '.join(('%s: %s' % (doc.type.name, doc.name) for doc in obj.documents.all()))

    def dehydrate_cities(self, obj):
        return ' / '.join(('%s' % city.name for city in obj.get_cities_intersected()))

    def dehydrate_states(self, obj):
        return '/'.join(('%s' % state.acronym for state in obj.get_states_intersected()))
