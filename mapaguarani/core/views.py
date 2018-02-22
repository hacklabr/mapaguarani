from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.gis.db.models.fields import GeometryField
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Count, Q
from django.views.generic import View
from django.http import JsonResponse
import rest_framework_gis
from rest_framework import viewsets, relations, serializers, generics
from rest_framework_serializer_field_permissions import fields
from collections import OrderedDict
from rest_pandas import PandasView
from boundaries.models import State, Country

from .models import (IndigenousLand, IndigenousVillage, MapLayer,
                     ArchaeologicalPlace, LandTenure, LandTenureStatus,
                     Project,)
from .serializers import (IndigenousLandSerializer, IndigenousVillageSerializer,
                          ArchaeologicalPlaceSerializer, ArchaeologicalPlaceExportSerializer,
                          SimpleArchaeologicalPlaceKMLSerializer,
                          LandTenureSerializer, LandTenureStatusSerializer,
                          IndigenousLandGeojsonSerializer, SimpleIndigenousLandKMLSerializer,
                          IndigenousVillageGeojsonSerializer, ArchaeologicalPlaceGeojsonSerializer,
                          LandTenureReportSerializer,
                          SimpleIndigenousGeojsonVillageSerializer,
                          SimpleIndigenousVillageKMLSerializer,
                          SimpleArchaeologicalPlaceGeojsonSerializer,
                          IndigenousVillageExportSerializer,
                          IndigenousLandExportSerializer, ProjectSerializer, )

from .renderers import KMLRenderer

from io import BytesIO
import zipfile
from fiona.crs import from_epsg
import fiona
import tempfile


class EmbeddableTemplateView(TemplateView):

    @method_decorator(xframe_options_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class ProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class KMLViewMixin(object):
    renderer_classes = (KMLRenderer,)

    def finalize_response(self, request, response, *args, **kwargs):
        self.headers['Content-Disposition'] = 'attachment; filename={}'.format(self.filename)
        response = super().finalize_response(request, response, *args, **kwargs)
        return response


class FilterLayersBySiteAndUserAuthenticatedMixin(object):

    def get_queryset(self):
        queryset = super(FilterLayersBySiteAndUserAuthenticatedMixin, self).get_queryset()

        # Filter layers according to current site
        current_site = get_current_site(self.request)
        layers = MapLayer.objects.filter(sites=current_site)
        queryset = queryset.filter(layer__in=layers)

        # Only show restricted features to authenticated users
        if not self.request.user.is_authenticated():
            queryset = queryset.filter(status='public')
            public_layers = MapLayer.objects.filter(status='public')
            queryset = queryset.filter(layer__in=public_layers)

        return queryset


class ArchaeologicalPlaceMixin(object):

    def get_queryset(self):
        queryset = super(ArchaeologicalPlaceMixin, self).get_queryset()

        if not self.request.user.is_authenticated():
            queryset = queryset.filter(status='public')

        return queryset


class IndigenousLandViewSet(FilterLayersBySiteAndUserAuthenticatedMixin, viewsets.ReadOnlyModelViewSet):
    queryset = IndigenousLand.objects.all()
    serializer_class = IndigenousLandSerializer


class IndigenousLandExportView(FilterLayersBySiteAndUserAuthenticatedMixin, PandasView):
    queryset = IndigenousLand.objects.all()
    serializer_class = IndigenousLandExportSerializer


class IndigenousLandKMLView(FilterLayersBySiteAndUserAuthenticatedMixin, KMLViewMixin, viewsets.ReadOnlyModelViewSet):
    queryset = IndigenousLand.objects.all()
    serializer_class = SimpleIndigenousLandKMLSerializer
    filename = 'indigenous_land.kml'


class ArchaeologicalPlaceExportView(FilterLayersBySiteAndUserAuthenticatedMixin, ArchaeologicalPlaceMixin, PandasView):
    queryset = ArchaeologicalPlace.objects.all()
    serializer_class = ArchaeologicalPlaceExportSerializer


class IndigenousVillageViewSet(FilterLayersBySiteAndUserAuthenticatedMixin, viewsets.ReadOnlyModelViewSet):
    queryset = IndigenousVillage.objects.all()
    serializer_class = IndigenousVillageSerializer


class IndigenousVillageGeojsonView(FilterLayersBySiteAndUserAuthenticatedMixin, viewsets.ReadOnlyModelViewSet):
    queryset = IndigenousVillage.objects.all()
    serializer_class = SimpleIndigenousGeojsonVillageSerializer


class IndigenousVillageKMLView(KMLViewMixin, IndigenousVillageGeojsonView):
    serializer_class = SimpleIndigenousVillageKMLSerializer
    filename = 'indigenous_village.kml'


class IndigenousVillageExportView(FilterLayersBySiteAndUserAuthenticatedMixin, PandasView):
    queryset = IndigenousVillage.objects.all()
    serializer_class = IndigenousVillageExportSerializer


class ArchaeologicalPlaceGeojsonView(FilterLayersBySiteAndUserAuthenticatedMixin, viewsets.ReadOnlyModelViewSet):
    queryset = ArchaeologicalPlace.objects.all()
    serializer_class = SimpleArchaeologicalPlaceGeojsonSerializer


class ArchaeologicalPlaceKMLView(KMLViewMixin, ArchaeologicalPlaceGeojsonView):
    serializer_class = SimpleArchaeologicalPlaceKMLSerializer
    filename = 'archaeological_places.kml'


class ArchaeologicalPlaceViewSet(FilterLayersBySiteAndUserAuthenticatedMixin, viewsets.ReadOnlyModelViewSet):
    queryset = ArchaeologicalPlace.objects.all()
    serializer_class = ArchaeologicalPlaceSerializer


class LandTenureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LandTenure.objects.all()
    serializer_class = LandTenureSerializer


class LandTenureStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LandTenureStatus.objects.all()
    serializer_class = LandTenureStatusSerializer


class ShapefileView(generics.GenericAPIView):

    serializer_class = None
    queryset = None
    readme = None
    geo_field = None
    file_name = ''
    geometry_type = ''

    ENGINE_FIONA_MAPPING = {
        serializers.CharField: "str",
        serializers.SerializerMethodField: "str",
        serializers.NullBooleanField: "str",
        serializers.BooleanField: "str",
        serializers.URLField: "str",
        serializers.ImageField: "str",
        serializers.PrimaryKeyRelatedField: "str",
        serializers.SlugRelatedField: "str",
        serializers.EmailField: "str",
        serializers.FileField: "str",
        serializers.SlugField: "str",
        serializers.IntegerField: "int",
        serializers.DecimalField: "float",
        serializers.FloatField: "float",
        serializers.DateField: "str",
        serializers.TimeField: "str",
        serializers.DateTimeField: "str",
        serializers.ChoiceField: "str",
        serializers.ReadOnlyField: "str",
        serializers.Field: "str",
        # rest_framework_serializer_field_permissions fields
        fields.ReadOnlyField: "str",
    }

    def _get_fiona_type(self, field_type):

        field_type = type(field_type)
        if field_type not in self.ENGINE_FIONA_MAPPING:
            raise AttributeError("Mapping not supported with Fiona.")

        fiona_type = self.ENGINE_FIONA_MAPPING[field_type]
        if fiona_type == "str":
            max_length = 255
            fiona_type += ":%s" % max_length

        return fiona_type

    def get(self, *args, **kwargs):

        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` "
            % self.__class__.__name__
        )

        queryset = self.get_queryset()
        layer = self.get_serializer(queryset, many=True)

        # first = self.queryset.first()
        # geometry_type = first.geometry.geom_type

        # FIXME take it from self.geo_field
        geo_field = None
        for field in self.queryset.model._meta.fields:
            if isinstance(field, GeometryField) and field.name == self.geo_field:
                geo_field = field

        crs = from_epsg(geo_field.srid)
        if self.geometry_type:
            geometry_type = self.geometry_type
        else:
            geometry_type = geo_field.geom_type

        serializer_fields = OrderedDict(layer.child.fields)
        properties = serializer_fields.copy()
        properties.pop(self.geo_field)

        for field_name, field_type in serializer_fields.items():
            if isinstance(field_type, relations.ManyRelatedField):
                raise AttributeError("All Many to Many fields should be exclude from serializer. Field: " + field_name)
            if not isinstance(field_type, rest_framework_gis.fields.GeometryField):
                properties[field_name] = self._get_fiona_type(field_type)

        schema = {"geometry": geometry_type,
                  "properties": properties}

        temp_file = tempfile.NamedTemporaryFile(suffix='.shp', mode='w+b')
        temp_file.close()
        with fiona.open(
                temp_file.name,
                mode='w',
                driver='ESRI Shapefile',
                crs=crs,
                schema=schema,
                encoding='iso-8859-1', ) as shapefile:
                # encoding='utf-8', ) as shapefile:

            shapefile.writerecords(layer.data['features'])

        buffer = BytesIO()
        zip = zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED)
        file_ext = ['shp', 'shx', 'prj', 'dbf']
        for item in file_ext:
            filename = '%s.%s' % (temp_file.name.replace('.shp', ''), item)
            zip.write(filename, arcname='%s.%s' % (self.file_name.replace('.shp', ''), item))
        if self.readme:
            zip.writestr('README.txt', self.readme)
        zip.close()
        buffer.flush()
        zip_stream = buffer.getvalue()
        buffer.close()

        # Stick it all in a django HttpResponse
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename=%s.zip' % self.file_name
        response['Content-length'] = str(len(zip_stream))
        response['Content-Type'] = 'application/zip'
        response.write(zip_stream)
        return response


class IndigenousLandsShapefileView(FilterLayersBySiteAndUserAuthenticatedMixin, ShapefileView):
    serializer_class = IndigenousLandGeojsonSerializer
    queryset = IndigenousLand.objects.all()
    # self.readme = readme
    geo_field = 'geometry'
    geometry_type = 'MultiPolygon'
    file_name = 'terras_indigenas'


class IndigenousVillagesShapefileView(FilterLayersBySiteAndUserAuthenticatedMixin, ShapefileView):
    serializer_class = IndigenousVillageGeojsonSerializer
    queryset = IndigenousVillage.objects.all()
    # self.readme = readme
    geo_field = 'geometry'
    geometry_type = 'Point'
    file_name = 'aldeias_indigenas'


class ArchaeologicalPlacesShapefileView(FilterLayersBySiteAndUserAuthenticatedMixin, ArchaeologicalPlaceMixin, ShapefileView):
    serializer_class = ArchaeologicalPlaceGeojsonSerializer
    queryset = ArchaeologicalPlace.objects.all()
    # self.readme = readme
    geo_field = 'geometry'
    geometry_type = 'Point'
    file_name = 'sitios_arqueologicos'


class LandTenureReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LandTenure.objects.annotate(
        total_lands_count=Count('indigenous_lands'),
    )
    serializer_class = LandTenureReportSerializer

class ReportView(View):

    def get(self, request, *args, **kwargs):

        data = {}
        data['states'] = ['RS', 'SC', 'PR', 'SP', 'MS', 'RJ', 'ES', 'TO', 'PA', 'MA']

        states = [State.objects.filter(acronym=acronym).first() for acronym in data['states']]
        brasil = Country.objects.get(name='Brasil')

        tenure_official = ['Declarada', 'Homologada', 'Regularizada',
                           'Delimitada']

        data['guarani_presence'] = {}
        data['no_guarani_presence'] = {}
        data['no_guarani_presence_inside_land'] = {}
        data['no_guarani_presence_outside_land'] = {}
        guarani_presence = IndigenousVillage.objects.filter(geometry__coveredby=brasil.geometry).filter(ethnic_groups__name='Guarani')
        no_guarani_presence = guarani_presence.filter(
            Q(guarani_presence_annual_series=None) | Q(guarani_presence_annual_series__presence=False)
        )
        # no_guarani_presence = guarani_presence.filter(guarani_presence_annual_series=None)

        guarani_presence = guarani_presence.exclude(
            Q(guarani_presence_annual_series=None) | Q(guarani_presence_annual_series__presence=False)
        )
        # guarani_presence = guarani_presence.exclude(guarani_presence_annual_series=None)

        no_guarani_presence_inside_land = no_guarani_presence
        no_guarani_presence_outside_land = no_guarani_presence
        no_guarani_presence_inside_land_count = 0
        no_guarani_presence_outside_land_count = 0
        for village in no_guarani_presence:
            if village.land.filter(land_tenure__name__in=tenure_official).count() > 0:
                no_guarani_presence_outside_land = no_guarani_presence_outside_land.exclude(id=village.id)
                no_guarani_presence_inside_land_count += 1
            else:
                no_guarani_presence_outside_land_count += 1
                no_guarani_presence_inside_land = no_guarani_presence_inside_land.exclude(id=village.id)
        data['guarani_presence_count'] = guarani_presence.count()
        data['no_guarani_presence_count'] = no_guarani_presence.count()
        data['no_guarani_presence_inside_land_count'] = no_guarani_presence_inside_land_count
        data['no_guarani_presence_outside_land_count'] = no_guarani_presence_outside_land_count

        data['guarani_lands'] = {}
        data['exclusive_guarani_lands'] = {}
        # Get all lands with Guarani (and possible others) ethnic groups and exclude
        guarani_lands = IndigenousLand.objects.filter(ethnic_groups__name='Guarani').exclude(land_tenure_status__name='Terra Original')
        exclusive_guarani_lands = guarani_lands
        for land in guarani_lands:
            if land.ethnic_groups.count() > 1:
                exclusive_guarani_lands = exclusive_guarani_lands.exclude(id=land.id)
        data['guarani_lands_count'] = guarani_lands.count()
        data['exclusive_guarani_lands_count'] = exclusive_guarani_lands.count()

        data['non_exclusive_guarani_lands'] = {}
        non_exclsive_guarani_lands = guarani_lands.exclude(
            id__in=[guarani_land.id for guarani_land in exclusive_guarani_lands]
        )
        data['non_exclusive_guarani_lands_count'] = non_exclsive_guarani_lands.count()

        for state in states:
            data['no_guarani_presence'][state.acronym] = no_guarani_presence.filter(geometry__coveredby=state.geometry).count()
            data['guarani_presence'][state.acronym] = guarani_presence.filter(geometry__coveredby=state.geometry).count()
            data['no_guarani_presence_inside_land'][state.acronym] = no_guarani_presence_inside_land.filter(geometry__coveredby=state.geometry).count()
            data['no_guarani_presence_outside_land'][state.acronym] = no_guarani_presence_outside_land.filter(geometry__coveredby=state.geometry).count()

            data['guarani_lands'][state.acronym] = guarani_lands.filter(geometry__intersects=state.geometry).count()
            data['exclusive_guarani_lands'][state.acronym] = exclusive_guarani_lands.filter(geometry__intersects=state.geometry).count()
            data['non_exclusive_guarani_lands'][state.acronym] = non_exclsive_guarani_lands.filter(geometry__intersects=state.geometry).count()


        data['exclusive_guarani_lands']['tenures'] = []
        for land_tenure in LandTenure.objects.all():
            tenure_data = {}
            tenure_data['name'] = land_tenure.name

            if land_tenure.name == 'Em estudo':
                tenure_exclusive_guarani_lands = exclusive_guarani_lands.filter(
                    Q(land_tenure=land_tenure) | Q(land_tenure_status__name='Terra Original em Estudo de Revisão')
                )
            else:
                tenure_exclusive_guarani_lands = exclusive_guarani_lands.filter(
                    land_tenure=land_tenure).exclude(land_tenure_status__name='Terra Original em Estudo de Revisão')

            tenure_data['total_lands_count'] = tenure_exclusive_guarani_lands.count()
            for state in states:
                tenure_data[state.acronym] = tenure_exclusive_guarani_lands.filter(geometry__coveredby=state.geometry).count()

            data['exclusive_guarani_lands']['tenures'].append(tenure_data)

        tenure_order = ['Sem Providências', 'Em estudo', 'Declarada',
                        'Homologada', 'Regularizada', 'Delimitada',
                        'Em processo de desapropriação ou aquisição', 'Desapropriada',
                        'Adquirida', ]

        def index_of(name):
            try:
                return tenure_order.index(name)
            except:
                return 10

        data['exclusive_guarani_lands']['tenures'].sort(
            key=lambda item: index_of(item['name'])
        )

        return JsonResponse(data)
