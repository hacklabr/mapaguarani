from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_serializer_field_permissions import fields
from rest_framework_serializer_field_permissions.serializers import FieldPermissionSerializerMixin
from rest_framework_serializer_field_permissions.permissions import IsAuthenticated
from .models import (IndigenousLand, IndigenousVillage, ArchaeologicalPlace, LandTenure, LandTenureStatus,
                     GuaraniPresence, Population, Project, )
from protected_areas.serializers import BaseProtectedAreaSerializers
from django.utils.translation import ugettext as _
from rest_framework_cache.serializers import CachedSerializerMixin
from rest_framework_cache.registry import cache_registry


class PopulationSerializer(serializers.ModelSerializer):

        class Meta:
            model = Population
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


class ProjectSerializer(serializers.ModelSerializer):

    indigenous_lands = SimpleIndigenousLandSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'files',
                  'links', 'indigenous_villages', 'indigenous_lands',
                  'organizations',]
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
                     'city', 'state', ]


class IndigenousLandListSerializer(BaseListSerializerMixin):

    exclude_field = ['villages', 'population',
                     # 'calculated_area',
                     'protected_areas_integral', 'protected_areas_conservation',
                     'cities', 'states', 'guarani_presence']


class ProtectedAreasMixinSerializer(serializers.ModelSerializer):

    protected_areas_integral = serializers.SerializerMethodField()
    protected_areas_conservation = serializers.SerializerMethodField()

    @staticmethod
    def get_protected_areas_integral(obj):
        if obj.protected_areas:
            return BaseProtectedAreaSerializers(obj.protected_areas.filter(type='PI'), many=True).data

    @staticmethod
    def get_protected_areas_conservation(obj):
        if obj.protected_areas:
            return BaseProtectedAreaSerializers(obj.protected_areas.filter(type='US'), many=True).data


class IndigenousPlaceExportSerializer(object):

    """
    This serializer is used to generate the shapefile
    """

    ethnic_groups = serializers.SerializerMethodField()
    prominent_subgroup = serializers.SerializerMethodField()
    layer = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    @staticmethod
    def get_ethnic_groups(obj):
        return ", ".join([ethnic_groups.name for ethnic_groups in obj.ethnic_groups.all()])

    @staticmethod
    def get_prominent_subgroup(obj):
        return ", ".join([prominent_sub.name for prominent_sub in obj.prominent_subgroup.all()])

    @staticmethod
    def get_layer(obj):
        if obj.layer:
            return obj.layer.name

    @staticmethod
    def get_country(obj):
        # FIXME
        return 'Brasil'


class IndigenousVillageSerializer(FieldPermissionSerializerMixin,
                                  ProtectedAreasMixinSerializer,
                                  CachedSerializerMixin):

    position_precision = serializers.SerializerMethodField()
    population = serializers.SerializerMethodField()
    guarani_presence = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    land = serializers.SerializerMethodField()
    projects = SimpleProjectSerializer(many=True)

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

    @staticmethod
    def get_villages(obj):
        return SimpleIndigenousVillageSerializer(obj.villages, many=True).data

    @staticmethod
    def get_city(obj):
        if obj.city:
            return obj.city.name

    @staticmethod
    def get_state(obj):
        if obj.state:
            return obj.state.name or obj.state.acronym

    @staticmethod
    def get_land(obj):
        if obj.land:
            land = obj.land[0]
            return SimpleIndigenousLandSerializer(land).data

cache_registry.register(IndigenousVillageSerializer)


class IndigenousVillageExportSerializer(IndigenousPlaceExportSerializer,
                                        IndigenousVillageSerializer,
                                        CachedSerializerMixin):
    """
    This serializer is used to generate the shapefile and xls
    """

    ethnic_groups = serializers.SerializerMethodField()
    prominent_subgroup = serializers.SerializerMethodField()
    layer = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    position_precision = serializers.SerializerMethodField()

    class Meta:
        model = IndigenousVillage
        # geo_field = 'geometry'
        # only the id field is excluded
        fields = ['id', 'name', 'other_names', 'land', 'guarani_presence', 'population',
                  'ethnic_groups', 'prominent_subgroup',
                  'city', 'state', 'country',
                  'position_source', 'position_precision', 'public_comments',
                  'private_comments', 'layer']

    @staticmethod
    def get_guarani_presence(obj):
        # FIXME translations
        try:
            presence = obj.guarani_presence_annual_series.latest()
            if presence.presence:
                return 'Sim (Fonte: {} - {})'.format(presence.source, presence.date.year)
            else:
                'Não (Fonte: {} - {})'.format(presence.source, presence.date.year)
        except GuaraniPresence.DoesNotExist:
            return _('No information')

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

    # @staticmethod
    # def get_city(obj):
    #     if obj.city:
    #         return obj.city.name

    # @staticmethod
    # def get_state(obj):
    #     if obj.state:
    #         return obj.state.name or obj.state.acronym

cache_registry.register(IndigenousVillageExportSerializer)


class IndigenousVillageGeojsonSerializer(GeoFeatureModelSerializer,
                                         IndigenousVillageExportSerializer,
                                         CachedSerializerMixin):
    """
    This serializer is used to generate the shapefile
    """

    cti_id = serializers.ReadOnlyField(source='id')

    class Meta:
        model = IndigenousVillage
        geo_field = 'geometry'
        # only the id field is excluded
        fields = ['name', 'other_names', 'land', 'guarani_presence', 'population',
                  'ethnic_groups', 'prominent_subgroup',
                  'city', 'state', 'country',
                  'position_source', 'position_precision', 'public_comments',
                  'private_comments', 'cti_id', 'layer']

cache_registry.register(IndigenousVillageGeojsonSerializer)


class SimpleIndigenousVillageSerializer(serializers.ModelSerializer):

    """
    This serializer is used in some relations fields in others serializers
    """
    class Meta:
        model = IndigenousVillage
        fields = ['id', 'name']


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


class IndigenousLandSerializer(FieldPermissionSerializerMixin, ProtectedAreasMixinSerializer):

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


class IndigenousLandGeojsonSerializer(IndigenousPlaceExportSerializer,
                                      GeoFeatureModelSerializer,
                                      IndigenousLandSerializer):

    """
    This serializer is used to generate the shapefile
    """

    documents = serializers.SerializerMethodField()
    population = serializers.SerializerMethodField()
    cti_id = fields.ReadOnlyField(source='id', permission_classes=(IsAuthenticated(), ))
    ethnic_groups = serializers.SerializerMethodField()
    prominent_subgroup = serializers.SerializerMethodField()
    layer = serializers.SerializerMethodField()
    # country = serializers.SerializerMethodField()

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
            return _('Yes')
        else:
            return _('No')


class ArchaeologicalPlaceSerializer(serializers.ModelSerializer):

    position_precision = serializers.SerializerMethodField()

    @staticmethod
    def get_position_precision(obj):
        if obj.position_precision:
            return dict(IndigenousVillage.POSITION_PRECISION).get(obj.position_precision)

    class Meta:
        model = ArchaeologicalPlace
        # list_serializer_class = ArchaeologicalPlaceListSerializer
        # exclude = ['geometry']
        depth = 1
        fields = '__all__'


class ArchaeologicalPlaceGeojsonSerializer(IndigenousPlaceExportSerializer):

    class Meta:
        model = ArchaeologicalPlace
        geo_field = 'geometry'
        exclude = ['id', 'ethnic_groups', 'prominent_subgroup', ]


class SimpleArchaeologicalPlaceGeojsonSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = ArchaeologicalPlace
        geo_field = 'geometry'
        fields = ['id', 'name', 'geometry']


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
