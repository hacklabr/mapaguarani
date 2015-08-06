from rest_framework import serializers
from rest_framework_gis import fields
from .models import IndigenousLand, IndigenousVillage, ArchaeologicalPlace
import json
# from django.contrib.gis.geos import GEOSGeometry


class CompactGeometryField(fields.GeometryField):

    def to_representation(self, value):
        if isinstance(value, dict) or value is None:
            return value

        simplify = 0.001

        geometry = value.simplify(tolerance=simplify, preserve_topology=True)

        return fields.GeoJsonDict(geometry)
        # data = {
        #     'type': geometry.geom_type,
        #     'coordinates': geometry.coords,
        # }

        # precision = 8
        # floatrepr = json.encoder.FLOAT_REPR
        # Monkey patch for float precision!
        # json.encoder.FLOAT_REPR = lambda o: format(o, '.%sf' % precision)

        # json_data = json.dumps(data)

        # json.encoder.FLOAT_REPR = floatrepr  # Restore

        # if isinstance(value, dict) or value is None:
        #     return value
        # return json_data


class IndigenousLandSerializer(serializers.ModelSerializer):

    polygon = CompactGeometryField()
    # polygon = fields.GeometrySerializerMethodField()

    # @staticmethod
    # def get_polygon(obj):
        # import ipdb;ipdb.set_trace()
        # data = (
        #     ('type', obj.polygon.geom_type),
        #     ('coordinates', obj.polygon.coords),
        #  )
        # precision = 2
        # floatrepr = json.encoder.FLOAT_REPR
        # if precision is not None:
        #     # Monkey patch for float precision!
        #     json.encoder.FLOAT_REPR = lambda o: format(o, '.%sf' % precision)
        # json_data = json.dumps(data)
        #
        # json.encoder.FLOAT_REPR = floatrepr  # Restore
        # return json_data
        # simplify = 0.0001
        # simplify = 0

        # return obj.polygon.simplify(tolerance=simplify, preserve_topology=True)

    class Meta:
        model = IndigenousLand



class IndigenousVillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndigenousVillage


class ArchaeologicalPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchaeologicalPlace
