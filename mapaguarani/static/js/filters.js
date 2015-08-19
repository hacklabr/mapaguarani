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

  filters.filter('listEthnic', [
    function() {
      return function(input, start) {
        if(input) {
          return _.map(input, function(g) { return g.name; }).join(', ');
        }
        return input;
      }
    }
  ])

})(angular);
