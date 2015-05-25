from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from djgeojson.views import GeoJSONLayerView
from core.models import IndigenousVillage
from django.conf import settings
admin.autodiscover()

urlpatterns = [
    url(r'^data.geojson$',
        GeoJSONLayerView.as_view(
            model=IndigenousVillage,
            geometry_field='position',
            properties=['name', 'other_names', 'ethnic_groups2', 'population', 'guarani_presence',]),
        name='villages'),
    url(r'^$', TemplateView.as_view(template_name='map.html'), name='home'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^rosetta/', include('rosetta.urls')),

]
