import json


class ResultLayerDataSerializer(object):
    """Serializer for GeoJSON result layers"""

    def __init__(self, options):

        self.options = options

        self.properties = options.get('properties', ['name',
                                                     'gen'])
        self.result_property = options.get('result_property', None)
        self.results_df = options.get('results_df', None)
        self.geometry_field = options.get('geometry_field', 'geom')
        self.srid = options.get('srid', 4326)

    def get_features(self, queryset):
        features = []
        for obj in queryset:
            # get geom field
            geom = getattr(obj, self.geometry_field)
            # transform to desired CRS if required
            if self.srid != geom.srid:
                geom.transform(self.srid)
            # get properties
            properties = {k: getattr(obj, k)
                          for k in self.properties}
            properties[self.result_property] =\
                self.options['results_df'][self.result_property].loc[obj.ags]
            properties['model'] = str(obj._meta)

            features.extend([{'type': 'Feature',
                              'properties': properties,
                              'id': obj.pk,
                              'geometry': json.loads(geom.geojson)
                              }
                             ])

        return features

    def serialize(self, queryset):
        """Serialize queryset"""

        geojson = {'type': 'FeatureCollection',
                   'features': self.get_features(queryset),
                   'crs': {
                       'type': 'link',
                       'properties': {'href': 'http://spatialreference.org/ref/epsg/4326/',
                                      "type": "proj4"}
                   }}

        return geojson
