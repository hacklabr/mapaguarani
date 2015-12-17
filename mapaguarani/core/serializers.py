from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import IndigenousLand, IndigenousVillage, ArchaeologicalPlace, LandTenure, LandTenureStatus
from protected_areas.serializers import BaseProtectedAreaSerializers


class SimpleIndigenousVillageSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndigenousVillage
        fields = ['id', 'name']


class IndigenousLandListSerializer(serializers.ListSerializer):

    exclude_field = ['villages', 'population', 'calculated_area', 'protected_areas', ]

    def __init__(self, *args, **kwargs):
        super(IndigenousLandListSerializer, self).__init__(*args, **kwargs)
        for field in self.exclude_field:
            self.child.fields.pop(field)


class IndigenousLandSerializer(serializers.ModelSerializer):

    associated_land = serializers.PrimaryKeyRelatedField(read_only=True)
    bbox = serializers.SerializerMethodField()
    guarani_presence = serializers.SerializerMethodField()
    villages = serializers.SerializerMethodField()
    population = serializers.ReadOnlyField()
    calculated_area = serializers.ReadOnlyField()
    protected_areas = serializers.SerializerMethodField()

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
    def get_protected_areas(obj):
        if obj.protected_areas:
            return BaseProtectedAreaSerializers(obj.protected_areas, many=True).data


class SimpleIndigenousLandSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndigenousLand
        fields = ['id', 'name']


class ListIndigenousVillageSerializer(serializers.ListSerializer):

    exclude_field = ['land', 'population', 'protected_areas', ]

    def __init__(self, *args, **kwargs):
        super(ListIndigenousVillageSerializer, self).__init__(*args, **kwargs)
        for field in self.exclude_field:
            self.child.fields.pop(field)


class IndigenousVillageSerializer(serializers.ModelSerializer):

    guarani_presence = serializers.ReadOnlyField()
    population = serializers.ReadOnlyField()
    land = serializers.SerializerMethodField()
    protected_areas = serializers.SerializerMethodField()

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
    def get_protected_areas(obj):
        if obj.protected_areas:
            return BaseProtectedAreaSerializers(obj.protected_areas, many=True).data


class ArchaeologicalPlaceListSerializer(serializers.ListSerializer):

    @classmethod
    def many_init(cls, *args, **kwargs):
        # Instantiate the child serializer.
        kwargs['child'] = cls()
        # Instantiate the parent list serializer.
        # import ipdb;ipdb.set_trace()
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

    ethnic_groups = serializers.SerializerMethodField()

    prominent_subgroup = serializers.SerializerMethodField()

    def get_ethnic_groups(self, obj):
        return " ".join([ethnic_groups.name for ethnic_groups in obj.ethnic_groups.all()])

    def get_prominent_subgroup(self, obj):
        return " ".join([prominent_sub.name for prominent_sub in obj.prominent_subgroup.all()])


class IndigenousLandGeojsonSerializer(IndigenousPlaceGeojsonSerializer):

    land_tenure = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    land_tenure_status = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = IndigenousLand
        geo_field = 'geometry'
        exclude = ['id', 'documents', 'layer', ]


class IndigenousVillageGeojsonSerializer(IndigenousPlaceGeojsonSerializer):

    class Meta:
        model = IndigenousVillage
        geo_field = 'geometry'
        fields = ['ethnic_groups', 'prominent_subgroup', 'population', 'guarani_presence', 'name', 'other_names',
        'public_comments', 'private_comments', 'position_precision', 'position_source', 'geometry']
        # exclude = ['id', 'layer', ]


class ArchaeologicalPlaceGeojsonSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = ArchaeologicalPlace
        geo_field = 'geometry'
        exclude = ['id', 'layer', ]


class LandTenureReportSerializer(serializers.ModelSerializer):
    total_lands = serializers.IntegerField()

    class Meta:
        model = LandTenure
        fields = ['id', 'name', 'map_color', 'total_lands', ]
