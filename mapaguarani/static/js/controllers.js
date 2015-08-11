(function(angular){
  'use strict';

  var controllers = angular.module('mapaguarani.controllers', []);

  controllers.controller('GuaraniMapCtrl', [
    '$scope',
    'GuaraniService',
    function ($scope, Guarani) {

      Guarani.villages.get({}, function(villages){
        $scope.villages = villages;
      });

      Guarani.lands.get({}, function(lands) {
        $scope.lands = lands;
      });

    }]
  );

})(angular);
