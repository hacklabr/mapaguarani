(function(angular, _) {
  'use strict';

  var services = angular.module('mapaguarani.services', [
    'ngResource'
  ]);

  services.factory('GuaraniService', [
    '$resource',
    function($resource) {
      return {
        villages: $resource('api/villages/:id'),
        lands: $resource('api/lands/:id'),
        toGeoJSON: function(data) {
          var geojson = {
            type: 'FeatureCollection',
            crs: {
              type: "link",
              properties: {
                type: "proj4",
                href: "http://spatialreference.org/ref/epsg/4326/"
              }
            },
            features: []
          };
          _.each(data, function(item) {
            var feature = {
              type: 'Feature',
              geometry: item.geometry,
              properties: {}
            };
            for(var key in item) {
              if(key !== 'geometry')
                feature.properties[key] = item[key];
            }
            geojson.features.push(feature);
          });
          return geojson;
        }
      }
    }
  ]);

})(angular, _);
