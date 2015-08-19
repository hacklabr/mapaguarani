from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
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

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),

    # Services
    url(r'^api/', include(router.urls)),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^rosetta/', include('rosetta.urls')),

]
