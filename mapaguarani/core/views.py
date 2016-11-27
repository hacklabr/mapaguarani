from django.http import HttpResponse
from django.views.generic import View
from django.contrib.gis.db.models.fields import GeometryField
from django.db.models import Count, F
import rest_framework_gis
from rest_framework import viewsets, relations, serializers, generics
from rest_framework_serializer_field_permissions import fields
from import_export import admin
from collections import OrderedDict

from .models import (IndigenousLand, IndigenousVillage,
                     ArchaeologicalPlace, LandTenure, LandTenureStatus,)
from .serializers import (IndigenousLandSerializer, IndigenousVillageSerializer,
                          ArchaeologicalPlaceSerializer, LandTenureSerializer,
                          LandTenureStatusSerializer, IndigenousLandGeojsonSerializer,
                          IndigenousVillageGeojsonSerializer, ArchaeologicalPlaceGeojsonSerializer,
                          LandTenureReportSerializer, SimpleIndigenousVillageSerializer,
                          SimpleIndigenousGeojsonVillageSerializer,
                          SimpleArchaeologicalPlaceGeojsonSerializer,)

from io import BytesIO
import zipfile
from fiona.crs import from_epsg
import fiona
import tempfile


IMPORT_EXPORT_FORMATS = [format().get_title() for format in admin.DEFAULT_FORMATS]


class IndigenousLandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IndigenousLand.objects.all()
    serializer_class = IndigenousLandSerializer


class IndigenousVillageMixin(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        queryset = super(IndigenousVillageMixin, self).get_queryset()
        queryset = queryset.filter(status='public')

        # TODO: refatorar para determinar camadas pelo dominio do site
        camadas_brasil = ['Guarani Sul e Sudeste - Aldeias', 'Guarani MS - Aldeias']
        camadas_la = ['Guarani Paraguai - Aldeias', 'Guarani Bolívia - Aldeias', 'Guarani Argentina - Aldeias']
        # import ipdb;ipdb.set_trace()
        if self.request.user.is_authenticated():
            camadas = camadas_brasil + camadas_la
        else:
            camadas = camadas_brasil
        queryset = queryset.filter(layer__name__in=camadas)

        return queryset


class IndigenousVillageViewSet(IndigenousVillageMixin):
    queryset = IndigenousVillage.objects.all()
    serializer_class = IndigenousVillageSerializer


class IndigenousVillageGeojsonView(IndigenousVillageMixin):
    queryset = IndigenousVillage.objects.all()
    serializer_class = SimpleIndigenousGeojsonVillageSerializer


class ArchaeologicalPlaceGeojsonView(viewsets.ReadOnlyModelViewSet):
    queryset = ArchaeologicalPlace.objects.all()
    serializer_class = SimpleArchaeologicalPlaceGeojsonSerializer


class ArchaeologicalPlaceViewSet(viewsets.ReadOnlyModelViewSet):
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
            try:
                max_length = field.max_length or 255
            except:
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
                raise AttributeError("All Many to Many fields should be exclude from serializer.")
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


class IndigenousLandsShapefileView(ShapefileView):
    serializer_class = IndigenousLandGeojsonSerializer
    queryset = IndigenousLand.objects.all()
    # self.readme = readme
    geo_field = 'geometry'
    geometry_type = 'MultiPolygon'
    file_name = 'terras_indigenas'


class IndigenousVillagesShapefileView(ShapefileView):
    serializer_class = IndigenousVillageGeojsonSerializer
    queryset = IndigenousVillage.objects.all()
    # self.readme = readme
    geo_field = 'geometry'
    geometry_type = 'Point'
    file_name = 'aldeias_indigenas'


class ArchaeologicalPlacesShapefileView(ShapefileView):
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


class IndigenousVillageReportExport(View):

    def get(self, request):
        format = request.GET.get('format', 'csv')
        if format not in IMPORT_EXPORT_FORMATS:
            format = 'csv'

        queryset = IndigenousVillage.objects.all()
        # resource = IndigenousVillageResource()
        from import_export import resources
        resource = resources.Resource()

        layer = IndigenousVillageGeojsonSerializer(queryset, many=True)
        import ipdb;ipdb.set_trace()
        resource.instance = layer.instance
        dataset = resource.export()

        response = HttpResponse(getattr(dataset, format), content_type=format)
        response['Content-Disposition'] = 'attachment; filename=filename.%s' % format
        return response
