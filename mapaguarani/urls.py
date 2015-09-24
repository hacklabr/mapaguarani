from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from djgeojson.views import TiledGeoJSONLayerView
from core.views import (IndigenousLandsLayerView, IndigenousLandViewSet, IndigenousVillageViewSet,
                        ArchaeologicalPlaceViewSet, LandTenureViewSet, LandTenureStatusViewSet,
                        IndigenousLandsShapefileView, IndigenousVillagesShapefileView,
                        ArchaeologicalPlacesShapefileView, )
from core.models import IndigenousVillage, IndigenousLand, ArchaeologicalPlace
from moderation.helpers import auto_discover
from rest_framework import routers


auto_discover()
admin.autodiscover()

router = routers.SimpleRouter()
router.register(r'lands', IndigenousLandViewSet)
router.register(r'land_tenures', LandTenureViewSet)
router.register(r'land_tenures_status', LandTenureStatusViewSet)
router.register(r'villages', IndigenousVillageViewSet)
router.register(r'archaeological', ArchaeologicalPlaceViewSet)

urlpatterns = [

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),

    # Services
    url(r'^api/', include(router.urls)),

    url(r'^tiles/villages/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).geojson$',
        TiledGeoJSONLayerView.as_view(
            model=IndigenousVillage,
            geometry_field='geometry',
            properties=['id', 'name',],
        ), name='data'),

    url(r'^tiles/lands/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).geojson$',
        TiledGeoJSONLayerView.as_view(
            model=IndigenousLand,
            geometry_field='geometry',
            properties=['id', 'name', 'land_tenure', 'land_tenure_status', ],
            trim_to_boundary=True,
            simplifications={
                0: 0.001,
                1: 0.001,
                2: 0.001,
                3: 0.001,
                4: 0.001,
                5: 0.001,
                6: 0.001,
                7: 0.001,
                8: 0.001,
                9: 0.001,
                # 10: 0.0001,
            }
        ), name='data'),

    url(r'^tiles/archaeological/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+).geojson$',
        TiledGeoJSONLayerView.as_view(
            model=ArchaeologicalPlace,
            geometry_field='geometry',
            properties=['id', 'name',],
        ), name='data'),

     url(r'^shapefiles/villages/$', IndigenousVillagesShapefileView.as_view(), name='villages_shapefiles'),

    url(r'^shapefiles/lands/$', IndigenousLandsShapefileView.as_view(), name='lands_shapefiles'),

    url(r'^shapefiles/archaeological/$', ArchaeologicalPlacesShapefileView.as_view(), name='archaeological_shapefiles'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^rosetta/', include('rosetta.urls')),

    url(r'^i18n/', include('django.conf.urls.i18n')),

]
