(function(angular, _) {
  'use strict';

  var services = angular.module('mapaguarani.services', [
    'ngResource'
  ]);

    services.factory('LandsReport', function($http) {
        return {
          get: function () {
            return $http.get('/api/lands_report');
          }
        };
    });

    services.factory('Project', function($resource){
        return $resource('/api/projects/:id/', {}, {
        });
    });

    services.factory('Villages', function($resource){
        return $resource('/api/villages/:id/', {}, {
          query: {
            method: 'GET',
            url: '/api/cached_villages/',
            isArray: true
          }
        });
    });

    services.factory('Pages', function($resource){
        return $resource('/api/pages/:id', {}, {
        });
    });

    services.factory('EthnicGroups', function($resource){
        return $resource('/api/ethnic_groups/:id', {}, {
        });
    });
    services.factory('ProminentEthnicGroups', function($resource){
        return $resource('/api/prominent_ethnic_subgroups/:id', {}, {
        });
    });

    services.factory('LandTenures', function($resource){
        return $resource('/api/land_tenures/:id', {}, {
        });
    });

  services.factory('GuaraniService', [
    '$q',
    '$window',
    '$resource',
    function($q, $window, $resource) {
      return {
        villages: $resource('/api/villages/:id', {}, {
          query: {
            method: 'GET',
            isArray: true,
            cache: true
          }
        }),
        lands: $resource('/api/lands/:id', {}, {
          query: {
            method: 'GET',
            isArray: true,
            cache: true
          }
        }),
        sites: $resource('/api/archaeological/:id', {}, {
          query: {
            method: 'GET',
            isArray: true,
            cache: true
          }
        }),
        tenures_report: $resource('/api/landtenurereport', {}, {
          query: {
            method: 'GET',
            isArray: true,
            cache: true
          }
        }),
        tenures_status: $resource('/api/land_tenures_status', {}, {
          query: {
            method: 'GET',
            isArray: true,
            cache: true
          }
        }),
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
