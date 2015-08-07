(function(angular){
  'use strict';

  var mapaguarani_services = angular.module('mapaguarani.services', ['ngResource']);

  mapaguarani_services.factory('IndigenousVillage', ['$resource',
  function($resource){
    return $resource('api/indigenous_villages', {}, {
    });
  }]);

  mapaguarani_services.factory('IndigenousLands', ['$resource',
  function($resource){
    return $resource('api/indigenous_lands', {}, {
    });
  }]);

})(angular);
