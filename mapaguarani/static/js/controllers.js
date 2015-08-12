(function(angular) {
  'use strict';

  var controllers = angular.module('mapaguarani.controllers', []);

  controllers.controller('HomeCtrl', [
    '$scope',
    'VillagesData',
    'LandsData',
    function ($scope, villages, lands) {

      $scope.filtered = {};

      $scope.villages = villages;
      $scope.lands = lands;

      $scope.mapData = {};

      $scope.$watch('filtered', function(filtered) {
        $scope.mapData.villages = filtered.villages;
        $scope.mapData.lands = filtered.lands;
      }, true);

    }]
  );

})(angular);
