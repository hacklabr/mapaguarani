from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import IndigenousLand, IndigenousVillage, ArchaeologicalPlace, LandTenure, LandTenureStatus


class IndigenousLandSerializer(serializers.ModelSerializer):

    associated_land = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = IndigenousLand
        exclude = ['polygon']
        depth = 1


class IndigenousVillageSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndigenousVillage
        exclude = ['position']
        depth = 1


class ArchaeologicalPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArchaeologicalPlace
        exclude = ['position']
        depth = 1


class LandTenureSerializer(serializers.ModelSerializer):

    class Meta:
        model = LandTenure
        fields = ['name', 'map_color', 'indigenous_lands']


class LandTenureStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = LandTenureStatus
        fields = ['name', 'map_color', 'indigenous_lands']


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
        geo_field = 'polygon'
        exclude = ['id', 'documents', 'layer', ]


class IndigenousVillageGeojsonSerializer(IndigenousPlaceGeojsonSerializer):

    class Meta:
        model = IndigenousVillage
        geo_field = 'position'
        fields = ['ethnic_groups', 'prominent_subgroup', 'population', 'guarani_presence', 'name', 'other_names',
        'public_comments', 'private_comments', 'position_precision', 'position_source', 'position']
        # exclude = ['id', 'layer', ]


class ArchaeologicalPlaceGeojsonSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = ArchaeologicalPlace
        geo_field = 'position'
        exclude = ['id', 'layer', ]
