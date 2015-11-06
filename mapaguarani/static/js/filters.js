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

  filters.filter('listObj', [
    function() {
      return function(input, prop) {
        if(input && input.length) {
          if(prop) {
            return _.map(input, function(g) { return g[prop]; }).join(', ');
          } else {
            return '';
          }
        }
        return '';
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

  filters.filter('advancedSearch', [
    function() {
      return function(input, filter, config) {
        if(filter && config) {
          for(var key in config) {
            if(filter[key]) {
              input = _.filter(input, function(item) {
                if(angular.isArray(item[key])) {
                  return _.find(item[key], function(propVal) {
                    return propVal[config[key].ref] == filter[key];
                  });
                } else {
                  if(item[key])
                    return item[key][config[key].ref] == filter[key];
                }
              });
            }
          }
        }
        return input;
      }
    }
  ])

})(angular, _);
