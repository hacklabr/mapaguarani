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
        villages: $resource('api/villages/:id', {}, {
          query: {
            method: 'GET',
            isArray: true,
            cache: true
          }
        }),
        lands: $resource('api/lands/:id', {}, {
          query: {
            method: 'GET',
            isArray: true,
            cache: true
          }
        }),
        sites: $resource('api/archaeological/:id', {}, {
          query: {
            method: 'GET',
            isArray: true,
            cache: true
          }
        }),
        tenures: $resource('api/land_tenures', {}, {
          query: {
            method: 'GET',
            isArray: true,
            cache: true
          }
        }),
        tenures_status: $resource('api/land_tenures_status', {}, {
          query: {
            method: 'GET',
            isArray: true,
            cache: true
          }
        }),
        getUniq: function(list, param, uniqParam) {
          var vals = [];
          _.each(list, function(item) {
            if(item[param]) {
              if(angular.isArray(item[param])) {
                if(item[param].length)
                  vals = vals.concat(item[param]);
              } else
                vals.push(item[param]);
            }
          });
          if(vals.length) {
            var uniq = _.uniq(vals, function(item, key) {
              if(typeof uniqParam !== 'undefined' && item[uniqParam]) {
                return item[uniqParam];
              } else {
                return item;
              }
            });
            return _.compact(uniq);
          } else {
            return [];
          }
        },
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

            var settings = _.extend({
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
                  options: settings
                }
              ]
            };
            $.ajax({
              type: 'POST',
              // url: 'http://localhost:4000/api',
              url: 'http://guarani.map.as:4000/api',
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
