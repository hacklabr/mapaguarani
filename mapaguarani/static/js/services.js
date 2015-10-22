(function(angular, _) {
  'use strict';

  var services = angular.module('mapaguarani.services', [
    'ngResource'
  ]);

  services.factory('GuaraniService', [
    '$q',
    '$resource',
    function($q, $resource) {
      return {
        villages: $resource('api/villages/:id'),
        lands: $resource('api/lands/:id'),
        sites: $resource('api/archaeological/:id'),
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
        },
        sqlTiles: function(name, options) {

          var deferred = $q.defer();

          $.get('/static/sql/' + name + '.html', function(html) {
            var sql = $(html).filter('#sql_template').html();
            var cartocss = $(html).filter('#cartocss_template').html();

            var options = _.extend({
              sql: sql,
              cartocss: cartocss,
              cartocss_version: '2.1.1',
              geom_column: 'geometry',
              geom_type: 'geometry'
            }, options || {});

            var data = {
              layers: [
                {
                  type: 'mapnik',
                  options: options
                }
              ]
            };
            $.ajax({
              type: 'POST',
              url: 'http://localhost:4000/api',
              data: JSON.stringify(data),
              contentType: 'application/json; charset=utf-8',
              dataType: 'json',
              success: function(data) {
                deferred.resolve(data.layergroupid);
              },
              error: function(jqXHR, textStatus, error) {
                console.log(error);
                deferred.reject(error);
              }
            });

          });

          return deferred.promise;
        }
      }
    }
  ]);

})(angular, _);
