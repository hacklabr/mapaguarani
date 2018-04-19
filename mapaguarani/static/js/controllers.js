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
          if($stateParams.x && $stateParams.y && $stateParams.z) {
            var x = parseFloat($stateParams.x);
            var y = parseFloat($stateParams.y);
            var z = parseFloat($stateParams.z);
            m.setView([x, y], z);
          }
          m.on('moveend', function(e) {
              if ($state.current.name === 'home') {
                $state.go('home', {x: m.getCenter()['lat'], y: m.getCenter()['lng'], z: m.getZoom()}, {notify: false});
              }
          });
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
    '$stateParams',
    'Data',
    'guaraniMapService',
    'GuaraniService',
    'user',
    function($state, $scope, $stateParams, data, Map, Guarani, user) {

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
          if($stateParams.x && $stateParams.y && $stateParams.z) {
            var x = parseFloat($stateParams.x);
            var y = parseFloat($stateParams.y);
            var z = parseFloat($stateParams.z);
            map.setView([x, y], z);
          } else if($scope.data.geometry) {
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
          map.on('moveend', function(e) {
              if ($state.current.name !== 'home') {
                var params = {id: $stateParams.id, x: map.getCenter()['lat'], y: map.getCenter()['lng'], z: map.getZoom(), notify: false};
                $state.go($state.current.name, params, {});
              }
          });
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
    'LandsReport',
    function($scope, LandsReport) {
      $scope.tenures = [];
      $scope.tenures_2nd_block = [];

      LandsReport.get().then(function(response) {
        $scope.report = response.data;
        angular.forEach($scope.report.exclusive_guarani_lands.tenures, function(item){
          if (item.name == 'Delimitada' || item.name == 'Declarada' ||
              item.name == 'Homologada' || item.name == 'Regularizada' ||
              item.name == 'Em estudo') {
            item.name = item.name + 's (incluindo revisão de limites)';
            $scope.tenures.push(item);
          } else if (item.name == 'Em processo de desapropriação ou aquisição' ||
              item.name == 'Desapropriada' || item.name == 'Adquirida' ) {
            $scope.tenures_2nd_block.push(item);
          } else {
            $scope.tenures.unshift(item);
          }
        });
      });
    }
  ]);

  controllers.controller('ProjectsCtrl', [
    '$scope',
    'Project',
    function($scope, Project) {
      $scope.projects = Project.query({}, function(projects) {
        $scope.projects = projects;
      });
    }
  ]);

})(angular, L, _);
