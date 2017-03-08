(function(angular, L, _) {
  'use strict';

  var controllers = angular.module('mapaguarani.controllers', ['ngSanitize']);

  controllers.controller('MainCtrl', [
    '$scope',
    function($scope) {

    }
  ]);

  controllers.controller('HomeCtrl', [
    '$scope',
    '$state',
    '$stateParams',
    'GuaraniService',
    'guaraniMapService',
    'user',
    function ($scope, $state, $stateParams, Guarani, Map, user) {

      // State dependencies resolved, emit event to hide loading message
      $scope.$emit('mapaguarani.loaded');

      // Init filtered results object
      $scope.filtered = {};

      function generate_urls(features, type) {
          angular.forEach(features, function(item){
              item.url = $state.href(type, {id: item.id}, {inherit: false});
          });
          return features;
      }

      // Store state resolved data on scope
      Guarani.villages.query({}, function(villages){
          $scope.villages = generate_urls(villages, 'village');
      })

      Guarani.lands.query({}, function(lands){
          $scope.lands = generate_urls(lands, 'land');
      })

      Guarani.sites.query({}, function(sites){
          $scope.sites = generate_urls(sites, 'site');
      })

      $scope.user = user;

      // Watch and store map from MapService
      var map;
      $scope.$watch(function() {
        return Map.getMap();
      }, function(m) {
        map = m;
      });

      // On state change update map bounds if state is home and "focus" is true
//      $scope.$on('$stateChangeSuccess', function(ev, to, toParams, from, fromParams) {
//        if(to.name == 'home' && fromParams.focus) {
//          Map.updateBounds();
//        }
//      });

      // Update state when viewing content is changed
      $scope.$on('mapaguarani.contentChanged', function(ev, content) {
        $state.go('home', {'content': content});
      });

      // Update state when viewing filter updates
      $scope.$on('mapaguarani.filterChanged', _.debounce(function(ev, filter) {
        $state.go('home', {'filter': JSON.stringify(filter)});
      }, 700));

      // Update state when page changes
      $scope.$on('mapaguarani.pageChanged', function(ev, page) {
        var param;
        if(page == 0) {
          param = null;
        } else {
          param = page+1;
        }
        $state.go('home', {'page': param});
      });
    }
  ]);

  controllers.controller('SingleCtrl', [
    '$state',
    '$scope',
    'Data',
    'guaraniMapService',
    'GuaraniService',
    'user',
    function($state, $scope, data, Map, Guarani, user) {

      // State dependencies resolved, emit event to hide loading message
      $scope.$emit('mapaguarani.loaded');

      // Store content type on scope
      $scope.type = $state.current.data.contentType;

      // Store resolved item data on scope
      $scope.data = data;
      $scope.map = {};
      $scope.map[$scope.type] = [$scope.data];
      $scope.user = user;

      // If focus, fit map bounds to item location
      // FIXME refactor this like there is no tomorrow
      if($state.params.focus) {
        $scope.$watch(function() {
          return Map.getMap();
        }, function(map) {
          if($scope.data.geometry) {
            var focusLayer = L.featureGroup();
            for(var key in $scope.map) {
              if($scope.map[key] && $scope.map[key].length) {
                console.log($scope.map[key]);
                L.geoJson(Guarani.toGeoJSON($scope.map[key])).addTo(focusLayer);
              }
            }
            map.fitBounds(focusLayer.getBounds());
            focusLayer = null;
          } else if($scope.data.bbox) {
            var bbox = $scope.data.bbox;
            map.fitBounds(L.latLngBounds([
              [bbox[1][1], bbox[0][0]],
              [bbox[0][1], bbox[0][0]]
            ]));
          }
        });
      }
    }
  ]);

    controllers.controller('SingleProjectCtrl', [
        '$state',
        '$scope',
        'Project',
        'guaraniMapService',
        'GuaraniService',
        'user',
        function($state, $scope, Project, guaraniMapService, GuaraniService, user) {

            // State dependencies resolved, emit event to hide loading message
            $scope.$emit('mapaguarani.loaded');

            $scope.project = Project.get({id: $state.params.id}, function(project){
                //  = project;
            });
        }
    ]);

  controllers.controller('LandTenureReportCtrl', [
    '$scope',
    'GuaraniService',
    function($scope, GuaraniService) {
      $scope.tenures = [];
      var query = window.query = GuaraniService.tenures_report.query();

      query && query.$promise.then(function(tenures){
        $scope.tenures = tenures;
      });

      $scope.tenures_sum = function(key) {
        return $scope.tenures.reduce(function(sum, tenure){
          return sum + (tenure[key] || 0);
        }, 0);
      };
    }
  ]);

})(angular, L, _);
