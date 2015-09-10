from rest_framework import serializers
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
