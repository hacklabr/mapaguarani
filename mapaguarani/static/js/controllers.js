(function(angular) {
  'use strict';

  var controllers = angular.module('mapaguarani.controllers', []);

  controllers.controller('HomeCtrl', [
    '$scope',
    '$state',
    'VillagesData',
    'LandsData',
    'SitesData',
    function ($scope, $state, villages, lands, sites) {

      $scope.filtered = {};

      $scope.villages = villages;
      $scope.lands = lands;
      $scope.sites = sites;
      
      $scope.mapData = {};

      $scope.$watch('filtered', function(filtered) {
        $scope.mapData.villages = filtered.villages;
        $scope.mapData.lands = filtered.lands;
        $scope.mapData.sites = filtered.sites;
      }, true);

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
    function($state, $scope, data) {
      $scope.type = $state.current.data.contentType;
      $scope.data = data;
      console.log($scope.data);
    }
  ]);

})(angular);
