from import_export import fields, resources
from core.models import IndigenousLand
from django.utils.translation import ugettext_lazy as _


class IndigenousVillageResource(resources.ModelResource):
    guarani_presence = fields.Field()

    class Meta:
        model = IndigenousLand
        fields = ('name', 'other_names', 'ethnic_groups', 'prominent_subgroup',
                  'official_area', 'land_tenure')
        export_order = ('name', 'other_names', 'ethnic_groups', 'prominent_subgroup',
                        'guarani_presence', 'official_area', 'land_tenure')

    def dehydrate_ethnic_groups(self, obj):
        return '; '.join(obj.ethnic_groups.values_list('name', flat=True))

    def dehydrate_prominent_subgroup(self, obj):
        return '; '.join(obj.prominent_subgroup.values_list('name', flat=True))

    def dehydrate_guarani_presence(self, obj):
        return _('Yes') if obj.population > 0 else _('No')
