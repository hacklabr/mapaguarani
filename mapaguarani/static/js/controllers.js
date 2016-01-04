(function(angular, L, _) {
  'use strict';

  var controllers = angular.module('mapaguarani.controllers', []);

  controllers.controller('MainCtrl', [
    '$scope',
    function($scope) {

    }
  ]);

  controllers.controller('HomeCtrl', [
    '$scope',
    '$state',
    '$stateParams',
    'VillagesData',
    'LandsData',
    'SitesData',
    'GuaraniService',
    'guaraniMapService',
    'user',
    function ($scope, $state, $stateParams, villages, lands, sites, Guarani, Map, user) {

      // State dependencies resolved, emit event to hide loading message
      $scope.$emit('mapaguarani.loaded');

      // Init filtered results object
      $scope.filtered = {};

      // Store state resolved data on scope
      $scope.lands = lands;
      $scope.villages = villages;
      $scope.sites = sites;
      $scope.user = user;

      // Watch and store map from MapService
      var map;
      $scope.$watch(function() {
        return Map.getMap();
      }, function(m) {
        map = m;
      });

      // On state change update map bounds if state is home and "focus" is true
//      $scope.$on('$stateChangeSuccess', function(ev, to, toParams, from, fromParams) {
//        if(to.name == 'home' && fromParams.focus) {
//          Map.updateBounds();
//        }
//      });

      // Update state when viewing content is changed
      $scope.$on('mapaguarani.contentChanged', function(ev, content) {
        $state.go('home', {'content': content});
      });

      // Update state when viewing filter updates
      $scope.$on('mapaguarani.filterChanged', _.debounce(function(ev, filter) {
        $state.go('home', {'filter': JSON.stringify(filter)});
      }, 700));

      // Update state when page changes
      $scope.$on('mapaguarani.pageChanged', function(ev, page) {
        var param;
        if(page == 0) {
          param = null;
        } else {
          param = page+1;
        }
        $state.go('home', {'page': param});
      });

      // Watch "clustered" params (related to cluster click) to show "area results"
      $scope.$watch(function() {
        return $state.params;
      }, function(params) {
        if(params.clustered) {
          var clustered = JSON.parse(params.clustered);
          if(clustered && clustered.ids.length) {
            $scope.clustered = _.filter($scope[clustered.type + 's'], function(item) { return clustered.ids.indexOf(item.id) !== -1; });
          } else {
            $scope.clustered = {};
          }
        } else {
          $scope.clustered = {};
        }
      });

      // Clear "area results"
      $scope.clearClustered = function() {
        $state.go('home', {clustered: null});
      };

    }
  ]);

  controllers.controller('SingleCtrl', [
    '$state',
    '$scope',
    'Data',
    'guaraniMapService',
    'GuaraniService',
    'user',
    function($state, $scope, data, Map, Guarani, user) {

      // State dependencies resolved, emit event to hide loading message
      $scope.$emit('mapaguarani.loaded');

      // Store content type on scope
      $scope.type = $state.current.data.contentType;

      // Store resolved item data on scope
      $scope.data = data;
      $scope.map = {};
      $scope.map[$scope.type] = [$scope.data];
      $scope.user = user;

      // If focus, fit map bounds to item location
      if($state.params.focus) {
        $scope.$watch(function() {
          return Map.getMap();
        }, function(map) {
          if($scope.data.geometry) {
            var focusLayer = L.featureGroup();
            for(var key in $scope.map) {
              if($scope.map[key] && $scope.map[key].length) {
                console.log($scope.map[key]);
                L.geoJson(Guarani.toGeoJSON($scope.map[key])).addTo(focusLayer);
              }
            }
            map.fitBounds(focusLayer.getBounds());
            focusLayer = null;
          } else if($scope.data.bbox) {
            var bbox = $scope.data.bbox;
            map.fitBounds(L.latLngBounds([
              [bbox[1][1], bbox[0][0]],
              [bbox[0][1], bbox[0][0]]
            ]));
          }
        });
      }
    }
  ]);

  controllers.controller('LandTenureReportCtrl', [
    '$scope',
    'GuaraniService',
    function($scope, GuaraniService) {
      $scope.tenures = [];
      var query = window.query = GuaraniService.tenures_report.query();

      query && query.$promise.then(function(tenures){
        $scope.tenures = tenures;
      });

      $scope.tenures_sum = function(key) {
        return $scope.tenures.reduce(function(sum, tenure){
          return sum + (tenure[key] || 0);
        }, 0);
      };
    }
  ]);

})(angular, L, _);
