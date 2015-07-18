from djgeojson.views import GeoJSONLayerView


class IndigenousLandsLayerView(GeoJSONLayerView):

    precision = 8   # float
    simplify = 0.001  # generalization