(function(angular){
  'use strict';

  var mapaguarani_controllers = angular.module('mapaguarani.controllers', []);

  mapaguarani_controllers.controller('GuaraniMapCtrl', ['$scope',
  'IndigenousVillage',
  'IndigenousLands',
  function ($scope, IndigenousVillage, IndigenousLands) {

    IndigenousVillage.get({}, function(villages){
      $scope.villages = villages;
    });

    IndigenousLands.get({}, function(lands) {
      $scope.lands = lands;
    });

  }
]);
})(angular);
