from djgeojson.views import GeoJSONLayerView
from rest_framework import viewsets
from .models import (IndigenousLand, IndigenousVillage,
                     ArchaeologicalPlace, LandTenure, LandTenureStatus,)
from .serializers import (IndigenousLandSerializer, IndigenousVillageSerializer,
                          ArchaeologicalPlaceSerializer, LandTenureSerializer,
                          LandTenureStatusSerializer)



class IndigenousLandsLayerView(GeoJSONLayerView):

    precision = 8   # float
    simplify = 0.001  # generalization


class IndigenousLandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IndigenousLand.objects.all()
    serializer_class = IndigenousLandSerializer


class IndigenousVillageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IndigenousVillage.objects.all()
    serializer_class = IndigenousVillageSerializer


class ArchaeologicalPlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArchaeologicalPlace.objects.all()
    serializer_class = ArchaeologicalPlaceSerializer


class LandTenureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LandTenure.objects.all()
    serializer_class = LandTenureSerializer


class LandTenureStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LandTenureStatus.objects.all()
    serializer_class = LandTenureStatusSerializer
