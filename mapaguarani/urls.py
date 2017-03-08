from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from core.views import (IndigenousLandViewSet, IndigenousVillageViewSet,
                        ArchaeologicalPlaceViewSet, LandTenureViewSet, LandTenureStatusViewSet,
                        IndigenousLandsShapefileView, IndigenousVillagesShapefileView,
                        ArchaeologicalPlacesShapefileView, LandTenureReportViewSet,
                        IndigenousVillageGeojsonView,
                        ArchaeologicalPlaceGeojsonView, IndigenousVillageExportView,
                        ProjectsViewSet,)
from moderation.helpers import auto_discover
from rest_framework import routers
from rest_framework_cache.registry import cache_registry
from rest_framework.urlpatterns import format_suffix_patterns


auto_discover()
admin.autodiscover()
cache_registry.autodiscover()

router = routers.SimpleRouter()
router.register(r'lands', IndigenousLandViewSet)
router.register(r'land_tenures', LandTenureViewSet)
router.register(r'land_tenures_status', LandTenureStatusViewSet)
router.register(r'villages', IndigenousVillageViewSet)
router.register(r'villages_geojson', IndigenousVillageGeojsonView)
router.register(r'arch_geojson', ArchaeologicalPlaceGeojsonView)
router.register(r'archaeological', ArchaeologicalPlaceViewSet)
router.register(r'landtenurereport', LandTenureReportViewSet)
router.register(r'projects', ProjectsViewSet)

urlpatterns = [

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),

    # Services
    url(r'^api/', include(router.urls)),

    url(r'^export/villages$', IndigenousVillageExportView.as_view(), name='export_xls_villages'),

    url(r'^shapefiles/villages/$', IndigenousVillagesShapefileView.as_view(), name='villages_shapefiles'),

    url(r'^shapefiles/lands/$', IndigenousLandsShapefileView.as_view(), name='lands_shapefiles'),

    url(r'^shapefiles/archaeological/$', ArchaeologicalPlacesShapefileView.as_view(), name='archaeological_shapefiles'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^rosetta/', include('rosetta.urls')),

    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^djangular.js',
        TemplateView.as_view(template_name='djangular.js', content_type='text/javascript'),
        name='djangular'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
