from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from .models import (
    IndigenousVillage, IndigenousLand, LegalProceedings, DocumentationType,
    Documentation, EthnicGroup, GuaraniPresence, Population,
    ArchaeologicalPlace,
)


@admin.register(IndigenousVillage)
class IndigenousVillageAdmin(admin.ModelAdmin):
    pass


@admin.register(IndigenousLand)
class IndigenousLandAdmin(geoadmin.GeoModelAdmin):
    display_wkt = True
    map_template = 'openlayers.html'
    list_display = ('name', 'other_names', 'official_area', 'claim', 'demand', 'source', 'land_tenure',
                    'land_tenure_status', 'public_comments', 'private_comments')
    list_editable = ('other_names', 'official_area', 'claim', 'demand', 'source', 'land_tenure',
                     'land_tenure_status', 'public_comments', 'private_comments')


@admin.register(LegalProceedings)
class LegalProceedingsAdmin(admin.ModelAdmin):
    pass


@admin.register(ArchaeologicalPlace)
class ArchaeologicalPlaceAdmin(admin.ModelAdmin):
    pass


admin.site.register(DocumentationType)
admin.site.register(Documentation)
admin.site.register(EthnicGroup)
admin.site.register(GuaraniPresence)
admin.site.register(Population)
