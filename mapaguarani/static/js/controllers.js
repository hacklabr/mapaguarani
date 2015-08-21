(function(angular, L, _) {
  'use strict';

  var controllers = angular.module('mapaguarani.controllers', []);

  controllers.controller('HomeCtrl', [
    '$scope',
    '$state',
    'VillagesData',
    'LandsData',
    'SitesData',
    'GuaraniService',
    'guaraniMapService',
    function ($scope, $state, villages, lands, sites, Guarani, Map) {

      $scope.filtered = {};

      $scope.villages = villages;
      $scope.lands = lands;
      $scope.sites = sites;

      Map.setData({
        villages: villages,
        lands: lands,
        sites: sites
      });

      $scope.mapData = {};

      var filter = false;

      var map;

      $scope.$watch(function() {
        return Map.getMap();
      }, function(m) {
        map = m;
      });

      $scope.$watch('filtered', _.debounce(function(filtered) {
        filter = filtered;
        if(map && $state.current.name == 'home') {
          var focusLayer = L.featureGroup();
          for(var key in filtered) {
            if(filtered[key] && filtered[key].length) {
              L.geoJson(Guarani.toGeoJSON(filtered[key])).addTo(focusLayer);
            }
          }
          map.fitBounds(focusLayer.getBounds());
          focusLayer = null;
        }
      }, 600), true);

      $scope.$on('$stateChangeSuccess', function(ev, to, toParams) {
        if(to.name == 'home') {
          Map.updateBounds();
        }
      });

      $scope.$on('mapaguarani.contentChanged', function(ev, content) {
        $state.go('home', {'content': content});
      });

      $scope.$on('mapaguarani.filterChanged', _.debounce(function(ev, filter) {
        $state.go('home', {'filter': JSON.stringify(filter)});
      }, 700));

      $scope.$on('mapaguarani.pageChanged', function(ev, page) {
        var param;
        if(page == 0) {
          param = null;
        } else {
          param = page+1;
        }
        $state.go('home', {'page': param});
      });

    }
  ]);

  controllers.controller('SingleCtrl', [
    '$state',
    '$scope',
    'Data',
    'guaraniMapService',
    'GuaraniService',
    function($state, $scope, data, Map, Guarani) {
      $scope.type = $state.current.data.contentType;
      $scope.data = data;
      $scope.map = {};
      $scope.map[$scope.type] = [$scope.data];
      $scope.$watch(function() {
        return Map.getMap();
      }, function(map) {
        var focusLayer = L.featureGroup();
        for(var key in $scope.map) {
          if($scope.map[key] && $scope.map[key].length) {
            L.geoJson(Guarani.toGeoJSON($scope.map[key])).addTo(focusLayer);
          }
        }
        map.fitBounds(focusLayer.getBounds());
        focusLayer = null;
      });

    }
  ]);

})(angular, L, _);
