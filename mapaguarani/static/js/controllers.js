(function(angular){
  'use strict';

  var controllers = angular.module('mapaguarani.controllers', []);

  controllers.controller('GuaraniMapCtrl', [
    '$scope',
    'GuaraniService',
    function ($scope, Guarani) {

      $scope.filtered = {};

      Guarani.villages.get({}, function(villages){
        $scope.villages = villages;
      });

      Guarani.lands.get({}, function(lands) {
        $scope.lands = lands;
      });

      $scope.mapData = {};

      $scope.$watch('filtered', function(filtered) {
        $scope.mapData.villages = filtered.villages;
        $scope.mapData.lands = filtered.lands;
      }, true);

    }]
  );

})(angular);
