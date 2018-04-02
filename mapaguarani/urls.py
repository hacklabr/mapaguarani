from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from core.views import (IndigenousLandViewSet, IndigenousVillageViewSet,
                        ArchaeologicalPlaceViewSet, LandTenureViewSet, LandTenureStatusViewSet,
                        IndigenousLandsShapefileView, IndigenousVillagesShapefileView,
                        ArchaeologicalPlaceKMLView,
                        ArchaeologicalPlacesShapefileView, ArchaeologicalPlaceExportView, LandTenureReportViewSet,
                        IndigenousVillageGeojsonView,
                        SimpleIndigenousVillageViewSetWithPosition,
                        ArchaeologicalPlaceGeojsonView, IndigenousVillageExportView, IndigenousVillageKMLView,
                        IndigenousLandExportView, IndigenousLandKMLView,
                        ProjectsViewSet,ReportView, EmbeddableTemplateView)
from rest_framework import routers
from rest_framework_cache.registry import cache_registry
from rest_framework.urlpatterns import format_suffix_patterns

from django.conf import settings

admin.autodiscover()
cache_registry.autodiscover()

router = routers.SimpleRouter()
router.register(r'lands', IndigenousLandViewSet)
router.register(r'land_tenures', LandTenureViewSet)
router.register(r'land_tenures_status', LandTenureStatusViewSet)
router.register(r'villages', IndigenousVillageViewSet)
router.register(r'simple_villages_with_position', SimpleIndigenousVillageViewSetWithPosition)
router.register(r'villages_geojson', IndigenousVillageGeojsonView)
router.register(r'lands_kml', IndigenousLandKMLView, base_name='lands-kml')
router.register(r'villages_kml', IndigenousVillageKMLView, base_name='villages-kml')
router.register(r'arch_kml', ArchaeologicalPlaceKMLView, base_name='arch-kml')
router.register(r'arch_geojson', ArchaeologicalPlaceGeojsonView)
router.register(r'archaeological', ArchaeologicalPlaceViewSet)
router.register(r'landtenurereport', LandTenureReportViewSet)
router.register(r'projects', ProjectsViewSet)

urlpatterns = [

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^embed/$', EmbeddableTemplateView.as_view(template_name='embed.html'), name='embed'),
    # Services
    url(r'^api/', include(router.urls)),

    url(r'^api/lands_report', ReportView.as_view(), name='report_view'),

    url(r'^export/villages$', IndigenousVillageExportView.as_view(), name='export_xls_villages'),

    url(r'^export/lands$', IndigenousLandExportView.as_view(), name='export_xls_lands'),

    url(r'^export/archaeological$', ArchaeologicalPlaceExportView.as_view(), name='export_xls_archaeological'),

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

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
