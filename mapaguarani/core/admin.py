from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from .models import (
    IndigenousVillage, IndigenousLand, LegalProceedings, DocumentType,
    Document, EthnicGroup, GuaraniPresence, Population,
    ArchaeologicalPlace,
)
from moderation.admin import ModerationAdmin


@admin.register(IndigenousVillage)
class IndigenousVillageAdmin(admin.ModelAdmin):
    list_per_page = 500


@admin.register(IndigenousLand)
class IndigenousLandAdmin(geoadmin.GeoModelAdmin, ModerationAdmin):
    # display_wkt = True
    map_template = 'openlayers.html'
    list_display = ('name', 'other_names', 'official_area', 'claim', 'demand', 'source', 'land_tenure',
                    'land_tenure_status', 'public_comments', 'private_comments')
    # list_editable = ('other_names', 'official_area', 'claim', 'demand', 'source', 'land_tenure',
    #                  'land_tenure_status', 'public_comments', 'private_comments')
    search_fields = ['name', 'other_names', 'claim', 'demand', 'source', 'land_tenure',
                    'land_tenure_status', 'public_comments', 'private_comments']
    list_per_page = 500


@admin.register(LegalProceedings)
class LegalProceedingsAdmin(admin.ModelAdmin):
    pass


@admin.register(ArchaeologicalPlace)
class ArchaeologicalPlaceAdmin(admin.ModelAdmin):
    list_per_page = 500


admin.site.register(DocumentType)
admin.site.register(Document)
admin.site.register(EthnicGroup)
admin.site.register(GuaraniPresence)
admin.site.register(Population)
