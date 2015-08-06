from djgeojson.views import GeoJSONLayerView
from rest_framework import viewsets
from .models import IndigenousLand, IndigenousVillage, ArchaeologicalPlace
from .serializers import IndigenousLandSerializer, IndigenousVillageSerializer, ArchaeologicalPlaceSerializer


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
