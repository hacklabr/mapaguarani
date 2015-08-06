from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from djgeojson.views import GeoJSONLayerView
from core.models import IndigenousVillage, IndigenousLand
from core.views import (IndigenousLandsLayerView, IndigenousLandViewSet, IndigenousVillageViewSet,
                        ArchaeologicalPlaceViewSet,)
from moderation.helpers import auto_discover
from rest_framework import routers


auto_discover()
admin.autodiscover()

router = routers.SimpleRouter()
router.register(r'lands', IndigenousLandViewSet)
router.register(r'villages', IndigenousVillageViewSet)
router.register(r'archaeological', ArchaeologicalPlaceViewSet)

urlpatterns = [
    url(r'^api/indigenous_villages$',
        GeoJSONLayerView.as_view(
            model=IndigenousVillage,
            geometry_field='position',
            properties=['name', 'other_names', 'ethnic_groups2', 'population', 'guarani_presence', ]),
        name='villages'),
    url(r'^api/indigenous_lands$',
        IndigenousLandsLayerView.as_view(
            model=IndigenousLand,
            geometry_field='polygon',
            properties=['name', 'other_names', 'guarani_exclusive_possession_area_portion',
                        'others_exclusive_possession_area_portion', 'claim', 'demand', 'source', 'land_tenure',
                        'land_tenure_status', 'associated_land', ]),
        name='lands'),

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),

    # Services
    url(r'^api/', include(router.urls)),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^rosetta/', include('rosetta.urls')),

]
