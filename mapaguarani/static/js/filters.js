(function(angular, _) {
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
      return function(input) {
        if(input) {
          return _.map(input, function(g) { return g.name; }).join(', ');
        }
        return input;
      }
    }
  ]);

  filters.filter('contentType', [
    function() {
      return function(input, contentType, filterContent, conditional) {
        if(contentType && conditional && contentType != filterContent) {
          return [];
        }
        return input;
      }
    }
  ]);

})(angular, _);
