(function(angular) {
  'use strict';

  var controllers = angular.module('mapaguarani.controllers', []);

  controllers.controller('HomeCtrl', [
    '$scope',
    '$state',
    'VillagesData',
    'LandsData',
    'SitesData',
    'guaraniMapService',
    function ($scope, $state, villages, lands, sites, Map) {

      $scope.filtered = {};

      $scope.villages = villages;
      $scope.lands = lands;
      $scope.sites = sites;

      $scope.mapData = {};

      var filter = false;

      if($state.current.name == 'home') {
        $scope.$watch('filtered', function(filtered) {
          filter = filtered;
          Map.setData(filtered);
        }, true);
      }

      $scope.$on('$stateChangeSuccess', function(ev, to, toParams, from) {
        if(filter && to.name == 'home') {
          Map.setData(filter);
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
    function($state, $scope, data, Map) {
      $scope.type = $state.current.data.contentType;
      $scope.data = data;
      $scope.map = {};
      $scope.map[$scope.type] = [$scope.data];
      Map.setData($scope.map);
    }
  ]);

})(angular);
