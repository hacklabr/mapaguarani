from django import forms
from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from django.utils.translation import ugettext_lazy as _
from .models import (
    IndigenousVillage, IndigenousLand, LegalProcedings, DocumentType,
    Document, EthnicGroup, ProminentEthnicSubGroup, GuaraniPresence, Population,
    ArchaeologicalPlace, ArchaeologicalImage, LandTenure, LandTenureStatus,
    MapLayer, Organization, ActionField, Project, ProjectFile, ProjectLink
)
from moderation.admin import ModerationAdmin
from mapwidgets.widgets import GooglePointFieldWidget
from django.contrib.gis.db import models
from rules.contrib.admin import ObjectPermissionsModelAdminMixin
from django.contrib.auth import get_permission_codename


class LayerPermissionsMixin(object):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        return qs.filter(layer__permission_groups__in=user.groups.all())

    def get_form(self, request, obj=None, **kwargs):
        form = super(LayerPermissionsMixin, self).get_form(request, obj, **kwargs)
        user = request.user
        form.base_fields['layer'].queryset = form.base_fields['layer'].queryset.filter(permission_groups__in=user.groups.all())
        return form

    def has_add_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('add', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))


class PopulationInLine(admin.TabularInline):
    model = Population


class GuaraniPresenceInLine(admin.TabularInline):
    model = GuaraniPresence


class IndigenousPlaceAdmin(LayerPermissionsMixin, ObjectPermissionsModelAdminMixin, ModerationAdmin):
    list_per_page = 500
    list_filter = ('layer', )
    list_editable = ('status',)

    def get_ethnic_groups(self, obj):
        return ", ".join([ethnic_group.name for ethnic_group in obj.ethnic_groups.all()])
    get_ethnic_groups.short_description = _('Ethnic Group')

    def get_prominent_subgroup(self, obj):
        return ", ".join([prominent_sub.name for prominent_sub in obj.prominent_subgroup.all()])
    get_prominent_subgroup.short_description = _('Prominent Ethnic SubGroup')


@admin.register(IndigenousVillage)
class IndigenousVillageAdmin(IndigenousPlaceAdmin):
    # extra_js = [GMAP.api_url + GMAP.key]
    # map_template = 'gis/admin/google.html'
    list_display = ('name', 'status', 'other_names', 'get_ethnic_groups', 'get_prominent_subgroup',
                    'population', 'get_guarani_presence',
                    'position_precision', 'position_source', 'geometry',
                    'public_comments', 'private_comments', )
    search_fields = ['name', 'other_names', ]
    filter_horizontal = ['ethnic_groups', 'prominent_subgroup', ]
    list_per_page = 500
    inlines = [
        PopulationInLine,
        GuaraniPresenceInLine,
    ]
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

    def get_guarani_presence(self, obj):
        return obj.guarani_presence
    get_guarani_presence.short_description = _('Guarani presence')
    get_guarani_presence.boolean = True

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].help_text = """Coloque aqui o nome pelo qual a própria comunidade reconhece a aldeia, sempre com primeira letra maíscula e as demais minúsculas """
        form.base_fields['other_names'].help_text = """Coloque aqui todos os outros nomes pelos quais a aldeia é conhecida, separados por vírgula """
        form.base_fields['ethnic_groups'].help_text = """Selecione o(s) povo(s) indígenas que habitam o local. """
        form.base_fields['prominent_subgroup'].help_text = """Preencha apenas se a aldeia tiver presença do povo guarani, qual(is) subgrupo(s) deste povo habita(m) o local."""
        form.base_fields['public_comments'].help_text = """Acrescente aqui informações textuais adicionais relevantes para o público amplo. Qualquer pessoa mesmo sem login poderá visualizá-las."""
        form.base_fields['private_comments'].help_text = """Acrescente aqui informações textuais adicionais relevantes para os administradores do site, como descrições de como foi localizada a aldeia, ou eventuais necessidades futuras de revisão de dados, e etc… Essas observações só serão visualizadas pelos administradores, colaboradores e editores logados. """
        form.base_fields['status'].help_text = """Você pode deixar essa aldeia restrita, para visualização apenas de pessoas logadas, ou pública, para visualização de qualquer visitante. """

        return form


@admin.register(IndigenousLand)
class IndigenousLandAdmin(geoadmin.GeoModelAdmin,
                          IndigenousPlaceAdmin):
    map_template = 'openlayers.html'
    filter_horizontal = ('ethnic_groups', 'prominent_subgroup', 'documents', )
    list_display = ('name', 'other_names', 'get_prominent_subgroup', 'official_area', 'claim', 'demand', 'source',
                    'land_tenure', 'land_tenure_status', 'public_comments', 'private_comments', 'associated_land',
                    'status',)
    # list_editable = ('other_names', 'official_area', 'claim', 'demand', 'source', 'land_tenure',
    #                  'land_tenure_status', 'public_comments', 'private_comments')

    search_fields = ['name', 'other_names', 'claim', 'demand', 'source', 'land_tenure__name',
                     'land_tenure_status__name', 'public_comments', 'private_comments']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].help_text =  """Coloque aqui o nome oficial pelo qual o Estado reconhece esta Terra Indígena"""
        form.base_fields['other_names'].help_text = """Coloque aqui todos os outros nomes pelos quais a Terra Indígena
                                                       é conhecida, separados por vírgula"""
        form.base_fields['ethnic_groups'].help_text = 'Selecione o(s) povo(s) indígenas que habitam o local.\n'
        form.base_fields['prominent_subgroup'].help_text = """Preencha apenas se a terra indígena tiver presença do 
                                                              povo guarani, qual(is) subgrupo(s) deste povo habita(m) o local."""
        form.base_fields['public_comments'].help_text = """Acrescente aqui informações textuais adicionais relevantes 
                                                           para o público amplo. Qualquer pessoa mesmo sem login 
                                                           poderá visualizá-las."""
        form.base_fields['private_comments'].help_text = """Acrescente aqui informações textuais adicionais relevantes 
                                                            para os administradores do site, como descrições de como foi 
                                                            desenhado o polígono da terra indígena, ou eventuais necessidades 
                                                            futuras de revisão de dados, e etc… Essas observações só serão 
                                                            visualizadas pelos administradores, colaboradores e editores logados."""
        form.base_fields['status'].help_text = """Você pode deixar essa terra indígena restrita, para visualização apenas 
                                                  de pessoas logadas, ou pública, para visualização de qualquer visitante."""
        return form


class ArchaeologicalImageInLine(admin.TabularInline):
    model = ArchaeologicalImage


@admin.register(ArchaeologicalPlace)
class ArchaeologicalPlaceAdmin(LayerPermissionsMixin, ObjectPermissionsModelAdminMixin, ModerationAdmin):
    list_display = ('get_name', 'acronym', 'cnsa', 'biblio_references',
                    'position_precision', 'position_comments', 'geometry', 'status',)
    list_editable = ('status',)
    search_fields = ['name', 'acronym', 'cnsa', 'biblio_references', ]
    list_per_page = 500
    inlines = [
        ArchaeologicalImageInLine,
    ]
    list_filter = ('layer', )
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

    def get_name(self, obj):
        if obj.name:
            return obj.name
        else:
            return _('(No name)')
    get_name.short_description = _('Name')


@admin.register(LegalProcedings)
class LegalProcedingsAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('indigenous_villages', 'indigenous_lands',
                         'archaeological_places', 'organizations',
                         'layers', 'files', 'links', )


admin.site.register(DocumentType)
admin.site.register(Document)
admin.site.register(EthnicGroup)
admin.site.register(ProminentEthnicSubGroup)
admin.site.register(LandTenure)
admin.site.register(LandTenureStatus)
admin.site.register(GuaraniPresence)
admin.site.register(Population)
admin.site.register(MapLayer)
admin.site.register(Organization)
admin.site.register(ActionField)
admin.site.register(ProjectLink)
admin.site.register(ProjectFile)
