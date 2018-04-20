from django.contrib.gis.shortcuts import compress_kml
from django.template import loader
from rest_framework.renderers import BaseRenderer, JSONRenderer
from spillway import collections

import mapbox_vector_tile


class TemplateRenderer(BaseRenderer):
    template_name = None

    def render(self, data, accepted_media_type=None, renderer_context=None):
        template = loader.get_template(self.template_name)
        return template.render({'features': data})


class KMLRenderer(TemplateRenderer):
    media_type = 'application/vnd.google-earth.kml+xml'
    format = 'kml'
    template_name = 'kml/placemarks.kml'


# class KMZRenderer(KMLRenderer):
#     media_type = 'application/vnd.google-earth.kmz'
#     format = 'kmz'
#
#     def render(self, *args, **kwargs):
#         kmldata = super().render(*args, **kwargs)
#         return compress_kml(kmldata)


class ProtobufRenderer(JSONRenderer):
    """Renderer which serializes to Protobuf.

    This renderer purposefully avoids reserialization of Protobuf from GeoJSON from the
    spatial backend which greatly improves performance.
    """
    media_type = 'vnd.mapbox-vector-tile'
    format = 'pbf'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Returns *data* encoded as GeoJSON."""

        if isinstance(data, list):
            data = collections.as_feature(data)

        data['name'] = renderer_context['view'].layer
        for index, features in enumerate(data['features']):
            data['features'][index]['name'] = renderer_context['view'].layer
        return mapbox_vector_tile.encode(data)
