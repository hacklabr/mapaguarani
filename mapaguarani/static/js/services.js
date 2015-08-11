(function(angular){
  'use strict';

  var services = angular.module('mapaguarani.services', ['ngResource']);

  services.factory('GuaraniService', [
    '$resource',
    function($resource) {
      return {
        villages: $resource('api/indigenous_villages'),
        lands: $resource('api/indigenous_lands')
      }
    }
  ]);

})(angular);
