from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_serializer_field_permissions import fields
from rest_framework_serializer_field_permissions.serializers import FieldPermissionSerializerMixin
from rest_framework_serializer_field_permissions.permissions import IsAuthenticated
from .models import (IndigenousLand, IndigenousVillage, ArchaeologicalPlace, LandTenure, LandTenureStatus,
                     GuaraniPresence, Population, Project, EthnicGroup, ProminentEthnicSubGroup)
from protected_areas.serializers import BaseProtectedAreaSerializers
from django.utils.translation import ugettext as _
from rest_framework_cache.serializers import CachedSerializerMixin
from rest_framework_cache.registry import cache_registry


class NamedCachedSerializerMixin(CachedSerializerMixin):

    def _get_cache_key(self, instance):
        request = self.context.get('request')
        protocol = request.scheme if request else 'http'
        serializer_name = self.Meta.cache_name
        params = {"id": instance.pk,
                  "app_label": instance._meta.app_label,
                  "model_name": instance._meta.object_name,
                  "serializer_name": serializer_name,
                  "protocol": protocol}
        return '{protocol}.{app_label}.{model_name}.{serializer_name}:{id}'.format(**params)


class PopulationSerializer(serializers.ModelSerializer):

        class Meta:
            model = Population
            fields = '__all__'


class EthnicGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = EthnicGroup
        fields = '__all__'


class ProminentEthnicSubGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProminentEthnicSubGroup
        fields = '__all__'

class GuaraniPresenceSerializer(serializers.ModelSerializer):

        class Meta:
            model = GuaraniPresence
            fields = '__all__'


class SimpleProjectSerializer(serializers.ModelSerializer):

        class Meta:
            model = Project
            fields = ['id', 'name', 'description', 'start_date', 'end_date', ]


class SimpleIndigenousLandSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndigenousLand
        fields = ['id', 'name']


class SimpleIndigenousLandKMLSerializer(CachedSerializerMixin, serializers.ModelSerializer):

    geometry = serializers.SerializerMethodField()

    class Meta:
        model = IndigenousLand
        fields = ['name', 'geometry']

    def get_geometry(self, obj):
        return obj.geometry.kml

cache_registry.register(SimpleIndigenousLandKMLSerializer)


class ProjectSerializer(serializers.ModelSerializer):

    indigenous_lands = SimpleIndigenousLandSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'files',
                  'links', 'indigenous_villages', 'indigenous_lands',
                  'organizations', 'archaeological_places',]
        depth = 1


class BaseListSerializerMixin(serializers.ListSerializer):

    """
    This class exclude the field listed in exclude_field variable when the serializer instance is a list.
    """

    exclude_field = []

    def __init__(self, *args, **kwargs):
        super(BaseListSerializerMixin, self).__init__(*args, **kwargs)
        for field in self.exclude_field:
            self.child.fields.pop(field)

    def update(self, instance, validated_data):
        super(BaseListSerializerMixin, self).update(instance, validated_data)


class ListIndigenousVillageSerializer(BaseListSerializerMixin):

    exclude_field = ['land', 'population', 'protected_areas_integral', 'protected_areas_conservation',
                     'cities', 'states', 'country', 'projects', 'layer_projects', ]


class IndigenousLandListSerializer(BaseListSerializerMixin):

    exclude_field = ['villages', 'population', 'layer', 'projects', 'layer_projects',
                     'guarani_exclusive_possession_area_portion',
                     'others_exclusive_possession_area_portion',
                     'protected_areas_integral', 'protected_areas_conservation', 'documents',
                     'cities', 'states', 'country', 'guarani_presence']


class ListArchaeologicalSiteSerializer(BaseListSerializerMixin):

    exclude_field = ['land', 'protected_areas_integral', 'protected_areas_conservation',
                     'cities', 'states', 'country', 'projects', 'layer_projects', ]


class GeoBaseMixinSerializer(serializers.ModelSerializer):

    protected_areas_integral = serializers.SerializerMethodField()
    protected_areas_conservation = serializers.SerializerMethodField()
    layer_projects = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    projects = SimpleProjectSerializer(many=True)

    @staticmethod
    def get_protected_areas_integral(obj):
        if obj.protected_areas:
            return BaseProtectedAreaSerializers(obj.protected_areas.filter(type='PI'), many=True).data

    @staticmethod
    def get_protected_areas_conservation(obj):
        if obj.protected_areas:
            return BaseProtectedAreaSerializers(obj.protected_areas.filter(type='US'), many=True).data

    @staticmethod
    def get_layer_projects(obj):
        if obj.layer_projects:
            return SimpleProjectSerializer(obj.layer_projects, many=True).data

    @staticmethod
    def get_country(obj):
        if obj.country:
            return obj.country.name


class PlaceExportSerializer(serializers.ModelSerializer):

    cities = serializers.SerializerMethodField()
    states = serializers.SerializerMethodField()
    layer = serializers.SerializerMethodField()

    @staticmethod
    def get_cities(obj):
        if obj.cities:
            return ', '.join([city.name for city in obj.cities.all()])

    @staticmethod
    def get_states(obj):
        if obj.states:
            return ', '.join([state.name for state in obj.states.all()])

    @staticmethod
    def get_layer(obj):
        if obj.layer:
            return obj.layer.name


class IndigenousPlaceExportSerializer(PlaceExportSerializer):

    """
    This serializer is used to generate the shapefile
    """

    ethnic_groups = serializers.SerializerMethodField()
    prominent_subgroup = serializers.SerializerMethodField()

    @staticmethod
    def get_ethnic_groups(obj):
        return ", ".join([ethnic_groups.name for ethnic_groups in obj.ethnic_groups.all()])

    @staticmethod
    def get_prominent_subgroup(obj):
        return ", ".join([prominent_sub.name for prominent_sub in obj.prominent_subgroup.all()])


class IndigenousVillageSerializer(FieldPermissionSerializerMixin,
                                  GeoBaseMixinSerializer):

    position_precision = serializers.SerializerMethodField()
    population = serializers.SerializerMethodField()
    guarani_presence = serializers.SerializerMethodField()
    projects = SimpleProjectSerializer(many=True)
    land = serializers.SerializerMethodField()

    # Private fields
    private_comments = fields.ReadOnlyField(permission_classes=(IsAuthenticated(), ))

    class Meta:
        model = IndigenousVillage
        list_serializer_class = ListIndigenousVillageSerializer
        depth = 1
        fields = '__all__'

    @staticmethod
    def get_position_precision(obj):
        if obj.position_precision:
            return dict(IndigenousVillage.POSITION_PRECISION).get(obj.position_precision)

    @staticmethod
    def get_population(obj):
        try:
            population = obj.population_annual_series.latest()
            return PopulationSerializer(population).data
        except Population.DoesNotExist:
            return None

    @staticmethod
    def get_guarani_presence(obj):
        try:
            presence = obj.guarani_presence_annual_series.latest()
        except GuaraniPresence.DoesNotExist:
            presence = GuaraniPresence(presence=False)

        return GuaraniPresenceSerializer(presence).data

    # @staticmethod
    # def get_villages(obj):
    #     return SimpleIndigenousVillageSerializer(obj.villages, many=True).data

    @staticmethod
    def get_land(obj):
        if obj.land:
            land = obj.land[0]
            return SimpleIndigenousLandSerializer(land).data


class IndigenousVillageCachedSerializer(IndigenousVillageSerializer,
                                        CachedSerializerMixin):

    class Meta:
        model = IndigenousVillage
        list_serializer_class = ListIndigenousVillageSerializer
        depth = 1
        fields = '__all__'

cache_registry.register(IndigenousVillageCachedSerializer)


class IndigenousVillageExportSerializer(IndigenousPlaceExportSerializer,
                                        IndigenousVillageSerializer,
                                        NamedCachedSerializerMixin):
    """
    This serializer is used to generate the shapefile and xls
    """
    def get_latitude(self, obj):
        if obj.geometry:
            return obj.geometry.get_y()
        else:
            return None

    def get_longitude(self, obj):
        if obj.geometry:
            return obj.geometry.get_x()
        else:
            return None

    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    ethnic_groups = serializers.SerializerMethodField()
    prominent_subgroup = serializers.SerializerMethodField()
    layer = serializers.SerializerMethodField()
    position_precision = serializers.SerializerMethodField()

    class Meta:
        cache_name = 'IndigenousVillageExportSerializer'
        model = IndigenousVillage
        fields = ['id', 'name', 'other_names', 'land', 'guarani_presence', 'population',
                  'ethnic_groups', 'prominent_subgroup',
                  'cities', 'states', 'country',
                  'position_precision', 'public_comments',
                  'private_comments', 'layer', 'latitude', 'longitude']

    @staticmethod
    def get_guarani_presence(obj):
        # FIXME translations
        try:
            presence = obj.guarani_presence_annual_series.latest()
            if presence.presence:
                return _('Currently Inhabited')
            else:
                return _('Old Villages, lands in use or dispossessed lands')
        except GuaraniPresence.DoesNotExist:
            return _('Old Villages, lands in use or dispossessed lands')

    @staticmethod
    def get_population(obj):
        try:
            population = obj.population_annual_series.latest()
            return _('{population} (Source: {source} - {year})').format(
                population=population.population,
                source=population.source,
                year=population.date.year
            )
        except Population.DoesNotExist:
            return _('No information')

    @staticmethod
    def get_position_precision(obj):
        if obj.position_precision:
            return str(dict(IndigenousVillage.POSITION_PRECISION).get(obj.position_precision))

    @staticmethod
    def get_land(obj):
        if obj.land:
            land = obj.land[0]
            return land.name

cache_registry.register(IndigenousVillageExportSerializer)


class IndigenousVillagePublicExportSerializer(IndigenousVillageExportSerializer):

    class Meta:
        cache_name = 'IndigenousVillagePublicExportSerializer'
        model = IndigenousVillage
        fields = ['id', 'name', 'other_names', 'land', 'guarani_presence', 'population',
                  'ethnic_groups', 'prominent_subgroup',
                  'cities', 'states', 'country',
                  'position_precision', 'public_comments',
                  'layer', 'latitude', 'longitude']

cache_registry.register(IndigenousVillagePublicExportSerializer)


class IndigenousVillageGeojsonSerializer(GeoFeatureModelSerializer,
                                         IndigenousVillageExportSerializer,
                                         CachedSerializerMixin):
    """
    This serializer is used to generate the shapefile
    """

    class Meta:
        model = IndigenousVillage
        geo_field = 'geometry'
        # only the id field is excluded
        fields = ['name', 'other_names', 'land', 'guarani_presence', 'population',
                  'ethnic_groups', 'prominent_subgroup',
                  'cities', 'states', 'country',
                  'position_precision', 'public_comments',
                  'private_comments', 'layer']

cache_registry.register(IndigenousVillageGeojsonSerializer)


class SimpleIndigenousVillageSerializer(serializers.ModelSerializer):

    """
    This serializer is used in some relations fields in others serializers
    """
    class Meta:
        model = IndigenousVillage
        fields = ['id', 'name']


class SimpleIndigenousVillageSerializerWithPosition(CachedSerializerMixin,
                                                    serializers.ModelSerializer):

    def get_latitude(self, obj):
        if obj.geometry:
            return obj.geometry.get_y()
        else:
            return None

    def get_longitude(self, obj):
        if obj.geometry:
            return obj.geometry.get_x()
        else:
            return None

    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    class Meta:
        model = IndigenousVillage
        fields = ['id', 'name', 'latitude', 'longitude']

cache_registry.register(SimpleIndigenousVillageSerializerWithPosition)


class SimpleIndigenousGeojsonVillageSerializer(GeoFeatureModelSerializer,
                                               CachedSerializerMixin):

    guarani_presence = serializers.SerializerMethodField()

    class Meta:
        model = IndigenousVillage
        geo_field = 'geometry'
        fields = ['id', 'name', 'guarani_presence', 'geometry']

    @staticmethod
    def get_guarani_presence(obj):
        try:
            presence = obj.guarani_presence_annual_series.latest()
        except GuaraniPresence.DoesNotExist:
            presence = GuaraniPresence(presence=False)

        return GuaraniPresenceSerializer(presence).data

cache_registry.register(SimpleIndigenousGeojsonVillageSerializer)


class SimpleIndigenousVillageKMLSerializer(CachedSerializerMixin, serializers.ModelSerializer):

    # guarani_presence = serializers.SerializerMethodField()
    geometry = serializers.SerializerMethodField()

    class Meta:
        model = IndigenousVillage
        # geo_field = 'geometry'
        fields = ['name', 'guarani_presence', 'geometry']

    @staticmethod
    def get_guarani_presence(obj):
        try:
            presence = obj.guarani_presence_annual_series.latest()
        except GuaraniPresence.DoesNotExist:
            presence = GuaraniPresence(presence=False)

        return GuaraniPresenceSerializer(presence).data

    def get_geometry(self, obj):
        return obj.geometry.kml

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        return repr

cache_registry.register(SimpleIndigenousVillageKMLSerializer)


class IndigenousLandSerializer(FieldPermissionSerializerMixin, GeoBaseMixinSerializer):

    associated_land = serializers.PrimaryKeyRelatedField(read_only=True)

    bbox = serializers.SerializerMethodField()
    guarani_presence = serializers.SerializerMethodField()
    villages = serializers.SerializerMethodField()

    population = serializers.ReadOnlyField()
    # calculated_area = serializers.ReadOnlyField()

    cities = serializers.SerializerMethodField()
    states = serializers.SerializerMethodField()

    private_comments = fields.ReadOnlyField(permission_classes=(IsAuthenticated(), ))
    claim = fields.ReadOnlyField(permission_classes=(IsAuthenticated(), ))
    demand = fields.ReadOnlyField(permission_classes=(IsAuthenticated(), ))
    projects = SimpleProjectSerializer(many=True)
    country = serializers.SerializerMethodField()

    class Meta:
        model = IndigenousLand
        list_serializer_class = IndigenousLandListSerializer
        exclude = ['geometry']
        depth = 1

    @staticmethod
    def get_bbox(obj):
        if obj.geometry.extent:
            return [[obj.geometry.extent[0], obj.geometry.extent[1]], [obj.geometry.extent[2], obj.geometry.extent[3]]]

    @staticmethod
    def get_guarani_presence(obj):
        guarani_presence = False
        # presences = []
        for village in obj.villages:
            try:
                presence = village.guarani_presence_annual_series.latest()
                guarani_presence = guarani_presence or presence.presence
                # presences.append(GuaraniPresenceSerializer(presence).data)
            except GuaraniPresence.DoesNotExist:
                pass

        return guarani_presence

    @staticmethod
    def get_villages(obj):
        return SimpleIndigenousVillageSerializer(obj.villages, many=True).data

    @staticmethod
    def get_cities(obj):
        cities = obj.get_cities_intersected()
        if cities:
            return ", ".join([city.name for city in cities])

    @staticmethod
    def get_states(obj):
        states = obj.get_states_intersected()
        if states:
            return ", ".join([state.name or state.acronym for state in states])

    @staticmethod
    def get_country(obj):
        if obj.country:
            return obj.country.name


class IndigenousLandExportSerializer(IndigenousPlaceExportSerializer,
                                     IndigenousLandSerializer,
                                     NamedCachedSerializerMixin):

    """
    This serializer is used to generate the shapefile
    """

    documents = serializers.SerializerMethodField()
    population = serializers.SerializerMethodField()
    ethnic_groups = serializers.SerializerMethodField()
    prominent_subgroup = serializers.SerializerMethodField()
    layer = serializers.SerializerMethodField()
    land_tenure = serializers.SerializerMethodField()
    land_tenure_status = serializers.SerializerMethodField()

    class Meta:
        model = IndigenousLand
        cache_name = 'IndigenousLandExportSerializer'
        fields = ['id', 'name', 'other_names', 'ethnic_groups', 'prominent_subgroup', 'villages', 'population',
                  'guarani_presence', 'official_area', 'land_tenure',
                  'land_tenure_status', 'associated_land',
                  'guarani_exclusive_possession_area_portion', 'others_exclusive_possession_area_portion',
                  'documents',
                  'cities', 'states', 'country', 'demand', 'claim', 'public_comments', 'source',
                  'private_comments', 'layer']

    @staticmethod
    def get_documents(obj):
        if obj.documents:
            return "; \n".join([document.description for document in obj.documents.all()])

    @staticmethod
    def get_population(obj):
        if obj.population == 0:
            return _('No information')
        else:
            return obj.population

    @staticmethod
    def get_villages(obj):
        if obj.villages:
            return ", ".join([village.name for village in obj.villages])

    @staticmethod
    def get_guarani_presence(obj):
        land_presence = False
        for village in obj.villages:
            try:
                presence = village.guarani_presence_annual_series.latest()
                land_presence = land_presence or presence.presence
            except GuaraniPresence.DoesNotExist:
                pass

        if land_presence:
            return _('Currently Inhabited')
        else:
            return _('Old Villages, lands in use or dispossessed lands')

    @staticmethod
    def get_land_tenure(obj):
        if obj.land_tenure:
            return obj.land_tenure.name

    @staticmethod
    def get_land_tenure_status(obj):
        if obj.land_tenure_status:
            return obj.land_tenure_status.name

cache_registry.register(IndigenousLandExportSerializer)


class IndigenousLandPublicExportSerializer(IndigenousLandExportSerializer):

    class Meta:
        model = IndigenousLand
        cache_name = 'IndigenousLandPublicExportSerializer'
        fields = ['id', 'name', 'other_names', 'ethnic_groups', 'prominent_subgroup', 'villages', 'population',
                  'guarani_presence', 'official_area', 'land_tenure',
                  'land_tenure_status', 'associated_land',
                  'guarani_exclusive_possession_area_portion', 'others_exclusive_possession_area_portion',
                  'documents',
                  'cities', 'states', 'country','public_comments', 'source', 'layer']

cache_registry.register(IndigenousLandPublicExportSerializer)


class IndigenousLandGeojsonSerializer(IndigenousLandExportSerializer,
                                      GeoFeatureModelSerializer,
                                      CachedSerializerMixin):

    # Trick to avoid fiona error
    cti_id = fields.ReadOnlyField(source='id', permission_classes=(IsAuthenticated(), ))

    class Meta:
        model = IndigenousLand
        geo_field = 'geometry'
        fields = ['cti_id', 'name', 'other_names', 'ethnic_groups', 'prominent_subgroup', 'villages', 'population',
                  'guarani_presence', 'official_area', 'land_tenure',
                  'land_tenure_status', 'associated_land',
                  'guarani_exclusive_possession_area_portion', 'others_exclusive_possession_area_portion',
                  'documents',
                  'cities', 'states', 'demand', 'claim', 'public_comments', 'source',
                  'private_comments', 'layer']

cache_registry.register(IndigenousLandGeojsonSerializer)


class IndigenousLandProtobufSerializer(IndigenousLandSerializer,
                                      GeoFeatureModelSerializer,
                                      CachedSerializerMixin):

    # Trick to avoid fiona error
    cti_id = fields.ReadOnlyField(source='id')
    land_tenure_map_color = serializers.SerializerMethodField()
    land_tenure_status_dashed_border = serializers.SerializerMethodField()

    class Meta:
        model = IndigenousLand
        geo_field = 'geometry'
        fields = ['cti_id', 'name', 'land_tenure_status_dashed_border' ,'land_tenure_map_color',]
        depth = 1

    @staticmethod
    def get_land_tenure_map_color(obj):
        if obj.land_tenure:
            return obj.land_tenure.map_color

    @staticmethod
    def get_land_tenure_status_dashed_border(obj):
        if obj.land_tenure_status:
            return obj.land_tenure_status.dashed_border

cache_registry.register(IndigenousLandProtobufSerializer)


class ArchaeologicalPlaceSerializer(GeoBaseMixinSerializer):

    position_precision = serializers.SerializerMethodField()
    land = serializers.SerializerMethodField()

    @staticmethod
    def get_position_precision(obj):
        if obj.position_precision:
            return dict(IndigenousVillage.POSITION_PRECISION).get(obj.position_precision)

    class Meta:
        model = ArchaeologicalPlace
        list_serializer_class = ListArchaeologicalSiteSerializer
        # exclude = ['geometry']
        depth = 1
        fields = '__all__'

    @staticmethod
    def get_land(obj):
        if obj.land:
            land = obj.land[0]
            return SimpleIndigenousLandSerializer(land).data


class ArchaeologicalPlaceExportSerializer(PlaceExportSerializer,
                                           ArchaeologicalPlaceSerializer):
    def get_latitude(self, obj):
        if obj.geometry:
            return obj.geometry.get_y()
        else:
            return None

    def get_longitude(self, obj):
        if obj.geometry:
            return obj.geometry.get_x()
        else:
            return None

    latitude = serializers.SerializerMethodField()

    longitude = serializers.SerializerMethodField()

    class Meta:
        model = ArchaeologicalPlace
        fields = ('id',
                  'name',
                  'acronym',
                  'cnsa',
                  'position_precision',
                  'position_comments',
                  'biblio_references',
                  'institution',
                  'hydrography',
                  'phase',
                  'dating',
                  'deviation',
                  'chrono_ref',
                  'ap_date',
                  'calibrated_dating',
                  'dating_method',
                  'lab_code',
                  'latitude',
                  'longitude',
                  'cities',
                  'country')


class ArchaeologicalPlaceGeojsonSerializer(PlaceExportSerializer,
                                           GeoBaseMixinSerializer,
                                           GeoFeatureModelSerializer,
                                           CachedSerializerMixin):

    class Meta:
        model = ArchaeologicalPlace
        geo_field = 'geometry'
        fields = ['ap_date',
                  'biblio_references',
                  'calibrated_dating',
                  'cities',
                  'country',
                  'dating',
                  'dating_method',
                  'name']


class SimpleArchaeologicalPlaceGeojsonSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = ArchaeologicalPlace
        geo_field = 'geometry'
        fields = ['id', 'name', 'geometry']


class SimpleArchaeologicalPlaceKMLSerializer(CachedSerializerMixin, serializers.ModelSerializer):

    geometry = serializers.SerializerMethodField()

    class Meta:
        model = ArchaeologicalPlace
        fields = ['name', 'geometry']

    def get_geometry(self, obj):
        return obj.geometry.kml

cache_registry.register(SimpleArchaeologicalPlaceKMLSerializer)


class LandTenureSerializer(serializers.ModelSerializer):

    class Meta:
        model = LandTenure
        fields = ['id', 'name', 'map_color', 'indigenous_lands']


class LandTenureStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = LandTenureStatus
        fields = ['id', 'name', 'map_color', 'dashed_border', 'indigenous_lands']


class LandTenureReportSerializer(serializers.ModelSerializer):
    total_lands_count = serializers.IntegerField()
    es_lands_count = serializers.IntegerField()
    pr_lands_count = serializers.IntegerField()
    rj_lands_count = serializers.IntegerField()
    rs_lands_count = serializers.IntegerField()
    sc_lands_count = serializers.IntegerField()
    sp_lands_count = serializers.IntegerField()

    class Meta:
        model = LandTenure
        fields = ['id', 'name', 'map_color', 'total_lands_count',
                  'es_lands_count', 'pr_lands_count', 'rj_lands_count',
                  'rs_lands_count', 'sc_lands_count', 'sp_lands_count', ]
