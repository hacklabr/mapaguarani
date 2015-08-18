(function(angular) {
  'use strict';

  var filters = angular.module('mapaguarani.filters', []);

  filters.filter('offset', [
    function() {
      return function(input, start) {
        if(input) {
          start = parseInt(start, 10);
          return input.slice(start);
        }
        return input;
      }
    }
  ]);

})(angular);
