from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from django.utils.translation import ugettext_lazy as _
from .models import (
    IndigenousVillage, IndigenousLand, LegalProceedings, DocumentType,
    Document, EthnicGroup, ProminentEthnicSubGroup, GuaraniPresence, Population,
    ArchaeologicalPlace, ArchaeologicalImage, LandTenure, LandTenureStatus
)
from moderation.admin import ModerationAdmin
# from django.contrib.gis.maps.google import GoogleMap
# GMAP = GoogleMap(key='AIzaSyDX4lCrBqaA-sXJTsm6NQhERpua6p-9SIQ') # Can also set GOOGLE_MAPS_API_KEY in settings


class PopulationInLine(admin.TabularInline):
    model = Population


@admin.register(IndigenousVillage)
class IndigenousVillageAdmin(geoadmin.GeoModelAdmin):
    # extra_js = [GMAP.api_url + GMAP.key]
    # map_template = 'gis/admin/google.html'

    list_display = ('name', 'other_names', 'get_ethnic_groups', 'get_prominent_subgroup',
                    'population', 'get_guarani_presence',
                    'position_precision', 'position_source', 'geometry',
                    'public_comments', 'private_comments',)
    search_fields = ['name', 'other_names',]
    list_per_page = 500
    inlines = [
        PopulationInLine,
    ]

    def get_guarani_presence(self, obj):
        return obj.guarani_presence
    get_guarani_presence.short_description = _('Guarani presence')
    get_guarani_presence.boolean = True

    def get_ethnic_groups(self, obj):
        return "\n".join([ethnic_group.name for ethnic_group in obj.ethnic_groups.all()])
    get_ethnic_groups.short_description = _('Ethnic Group')

    def get_prominent_subgroup(self, obj):
        return "\n".join([prominent_sub.name for prominent_sub in obj.prominent_subgroup.all()])
    get_prominent_subgroup.short_description = _('Prominent Ethnic SubGroup')


@admin.register(IndigenousLand)
class IndigenousLandAdmin(geoadmin.GeoModelAdmin, ModerationAdmin):
    # display_wkt = True
    map_template = 'openlayers.html'
    list_display = ('name', 'other_names', 'get_prominent_subgroup', 'official_area', 'claim', 'demand', 'source',
                    'land_tenure', 'land_tenure_status', 'public_comments', 'private_comments', 'associated_land')
    # list_editable = ('other_names', 'official_area', 'claim', 'demand', 'source', 'land_tenure',
    #                  'land_tenure_status', 'public_comments', 'private_comments')
    search_fields = ['name', 'other_names', 'claim', 'demand', 'source', 'land_tenure__name',
                     'land_tenure_status__name', 'public_comments', 'private_comments']
    list_per_page = 500

    def get_prominent_subgroup(self, obj):
        return "\n".join([prominent_sub.name for prominent_sub in obj.prominent_subgroup.all()])
    get_prominent_subgroup.short_description = _('Prominent Ethnic SubGroup')


class ArchaeologicalImageInLine(admin.TabularInline):
    model = ArchaeologicalImage


@admin.register(ArchaeologicalPlace)
class ArchaeologicalPlaceAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'code', 'acronym', 'cnsa', 'biblio_references',
                    'position_precision', 'position_comments', 'geometry',)
    search_fields = ['name', 'code', 'acronym', 'cnsa', 'biblio_references',]
    list_per_page = 500
    inlines = [
        ArchaeologicalImageInLine,
    ]

    def get_name(self, obj):
        if obj.name:
            return obj.name
        else:
            return _('(No name)')
    get_name.short_description = _('Name')


@admin.register(LegalProceedings)
class LegalProceedingsAdmin(admin.ModelAdmin):
    pass


admin.site.register(DocumentType)
admin.site.register(Document)
admin.site.register(EthnicGroup)
admin.site.register(ProminentEthnicSubGroup)
admin.site.register(LandTenure)
admin.site.register(LandTenureStatus)
admin.site.register(GuaraniPresence)
admin.site.register(Population)
