from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import (IndigenousLand, IndigenousVillage, ArchaeologicalPlace, LandTenure, LandTenureStatus,
                    GuaraniPresence, Population,)
from protected_areas.serializers import BaseProtectedAreaSerializers


class SimpleIndigenousVillageSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndigenousVillage
        fields = ['id', 'name']


class PopulationSerializer(serializers.ModelSerializer):

        class Meta:
            model = Population


class GuaraniPresenceSerializer(serializers.ModelSerializer):

        class Meta:
            model = GuaraniPresence


class IndigenousLandListSerializer(serializers.ListSerializer):

    exclude_field = ['villages', 'population', 'calculated_area',
                     'protected_areas_integral', 'protected_areas_conservation',
                     'cities', 'states', ]

    def __init__(self, *args, **kwargs):
        super(IndigenousLandListSerializer, self).__init__(*args, **kwargs)
        for field in self.exclude_field:
            self.child.fields.pop(field)


class IndigenousPlaceSerializer(serializers.ModelSerializer):

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


class IndigenousLandSerializer(IndigenousPlaceSerializer):

    associated_land = serializers.PrimaryKeyRelatedField(read_only=True)
    bbox = serializers.SerializerMethodField()
    guarani_presence = serializers.SerializerMethodField()
    villages = serializers.SerializerMethodField()
    population = serializers.ReadOnlyField()
    calculated_area = serializers.ReadOnlyField()

    cities = serializers.SerializerMethodField()
    states = serializers.SerializerMethodField()

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
        return obj.ethnic_groups.filter(name='Guarani').exists()

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


class SimpleIndigenousLandSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndigenousLand
        fields = ['id', 'name']


class ListIndigenousVillageSerializer(serializers.ListSerializer):

    exclude_field = ['land', 'population', 'protected_areas_integral', 'protected_areas_conservation',
                     'city', 'state', ]

    def __init__(self, *args, **kwargs):
        super(ListIndigenousVillageSerializer, self).__init__(*args, **kwargs)
        for field in self.exclude_field:
            self.child.fields.pop(field)


class IndigenousVillageSerializer(IndigenousPlaceSerializer):

    land = serializers.SerializerMethodField()
    protected_areas_integral = serializers.SerializerMethodField()
    protected_areas_conservation = serializers.SerializerMethodField()
    position_precision = serializers.SerializerMethodField()
    population = serializers.SerializerMethodField()
    guarani_presence = serializers.SerializerMethodField()

    city = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    class Meta:
        model = IndigenousVillage
        list_serializer_class = ListIndigenousVillageSerializer
        depth = 1

    @staticmethod
    def get_land(obj):
        if obj.land:
            land = obj.land[0]
            return SimpleIndigenousLandSerializer(land).data

    @staticmethod
    def get_position_precision(obj):
        if obj.position_precision:
            return dict(IndigenousVillage.POSITION_PRECISION).get(obj.position_precision)

    @staticmethod
    def get_population(obj):
        try:
            population = obj.population_annual_series.latest()
        except Population.DoesNotExist:
            # FIXME
            population = Population(population=0)

        return PopulationSerializer(population).data

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


class ArchaeologicalPlaceListSerializer(serializers.ListSerializer):

    @classmethod
    def many_init(cls, *args, **kwargs):
        # Instantiate the child serializer.
        kwargs['child'] = cls()
        # Instantiate the parent list serializer.
        return ArchaeologicalPlaceListSerializer(*args, **kwargs)

    class Meta:
        model = ArchaeologicalPlace
        depth = 1


class ArchaeologicalPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArchaeologicalPlace
        # list_serializer_class = ArchaeologicalPlaceListSerializer
        # exclude = ['geometry']
        depth = 1


class LandTenureSerializer(serializers.ModelSerializer):

    class Meta:
        model = LandTenure
        fields = ['id', 'name', 'map_color', 'indigenous_lands']


class LandTenureStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = LandTenureStatus
        fields = ['id', 'name', 'map_color', 'dashed_border', 'indigenous_lands']


class IndigenousPlaceGeojsonSerializer(GeoFeatureModelSerializer):

    """
    This serializer is used to generate the shapefile
    """

    cti_id = serializers.ReadOnlyField(source='id')
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
        return 'Brasil'
        # TODO: Verificar se uma terra indigena pode ter mais de um pais
        # if countries:
        #     return ", ".join([country.name for country in countries])


class IndigenousLandGeojsonSerializer(IndigenousPlaceGeojsonSerializer):

    """
    This serializer is used to generate the shapefile
    """

    land_tenure = serializers.SlugRelatedField(read_only=True, slug_field='name')
    land_tenure_status = serializers.SlugRelatedField(read_only=True, slug_field='name')
    documents = serializers.SerializerMethodField()
    cities = serializers.SerializerMethodField()
    states = serializers.SerializerMethodField()
    villages = serializers.SerializerMethodField()
    # guarani_presence = serializers.SerializerMethodField()

    class Meta:
        model = IndigenousLand
        geo_field = 'geometry'

    @staticmethod
    def get_documents(obj):
        if obj.documents:
            return "\n".join([document.description for document in obj.documents.all()])
            # return obj.documents.description

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
    def get_villages(obj):
        if obj.villages:
            return ", ".join([village.name for village in obj.villages])


class IndigenousVillageGeojsonSerializer(IndigenousPlaceGeojsonSerializer):

    """
    This serializer is used to generate the shapefile
    """

    guarani_presence = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    class Meta:
        model = IndigenousVillage
        geo_field = 'geometry'
        # fields = ['ethnic_groups', 'prominent_subgroup', 'population', 'guarani_presence', 'name', 'other_names',
        # 'public_comments', 'private_comments', 'position_precision', 'position_source', 'geometry']
        # exclude = ['id', 'layer', ]

    @staticmethod
    def get_guarani_presence(obj):
        try:
            presence = obj.guarani_presence_annual_series.latest()
            if presence.presence:
                return 'Sim (Fonte: {})'.format(presence.source)
            else:
                'Não (Fonte: {})'.format(presence.source)
        except GuaraniPresence.DoesNotExist:
            return ''

    @staticmethod
    def get_city(obj):
        if obj.city:
            return obj.city.name

    @staticmethod
    def get_state(obj):
        if obj.state:
            return obj.state.name or obj.state.acronym

class ArchaeologicalPlaceGeojsonSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = ArchaeologicalPlace
        geo_field = 'geometry'
        exclude = ['id', 'layer', ]


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
