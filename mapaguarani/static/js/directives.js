(function(angular, L, _) {
  'use strict';

  var directives = angular.module('mapaguarani.directives', []);

  directives.directive('sidebarHeight', [
    function() {
      return {
        restrict: 'A',
        scope: {
          sidebarHeight: '='
        },
        link: function(scope, element, attrs) {
          scope.$watch('sidebarHeight', function(apply) {
            doHeight(apply);
          });
          function doHeight(apply) {
            if(apply) {
              var height = $('#sidebar').height() - (57*4) - 64;
              $(element).height(height).addClass('active');
            } else {
              $(element).height(0).removeClass('active');;
            }
          }
        }
      }
    }
  ]);

  //Google maps - leaflet 0.7 only
  var gm_roadmap = new L.Google('ROADMAP');
  var gm_terrain = new L.Google('TERRAIN');
  var gm_hybrid = new L.Google('HYBRID');

  // Mapbox - leaflet 1.0 compatible
  var access_token = 'pk.eyJ1IjoiYnJ1bm9zbWFydGluIiwiYSI6IjM1MTAyYTJjMWQ3NmVmYTg0YzQ0ZWFjZTg0MDZiYzQ3In0.ThelegmeGkO5Vwd6KTu6xA';
  var mapbox_url = 'http://api.tiles.mapbox.com/v4/{mapid}/{z}/{x}/{y}.png?access_token={access_token}';
  var mapbox_satellite = L.tileLayer(mapbox_url, {mapid: 'mapbox.satellite', access_token: access_token});
  var mapbox_streets   = L.tileLayer(mapbox_url, {mapid: 'mapbox.streets', access_token: access_token});
  var mapbox_hybrid   = L.tileLayer(mapbox_url, {mapid: 'mapbox.streets-satellite', access_token: access_token});

  directives.directive('guaraniList', [
    '$rootScope',
    '$stateParams',
    function($rootScope, $stateParams) {
      return {
        restrict: 'E',
        scope: {
          villages: '=',
          lands: '=',
          sites: '=',
          filtered: '='
        },
        templateUrl: '/static/views/partials/list.html',
        link: function(scope, element, attrs) {

          /*
           * Content type
           */
          scope.content = $stateParams.content || '';
          scope.setContent = function(content) {
            scope.content = content;
            scope.curPage = 0;
          };
          scope.toggleContent = function(content) {
            if(scope.content == content) {
              scope.content = '';
            } else {
              scope.setContent(content);
            }
          }
          scope.$watch('content', function(content, prevContent) {
            if(content !== prevContent)
              $rootScope.$broadcast('mapaguarani.contentChanged', content);
          });

          scope.toggleLayer = function(layer) {

          };

          /*
           * Filters
           */
          scope.filtered = scope.filtered || {};

          scope.getAll = function() {
            var all = [];
            all = all.concat(angular.copy(scope.villages));
            all = all.concat(angular.copy(scope.lands));
            all = all.concat(angular.copy(scope.sites));
            return all;
          };

          scope.$watch('villages', function(villages) {
            if(typeof villages == 'object')
              scope.filtered.villages = angular.copy(villages);
          });

          scope.$watch('lands', function(lands) {
            if(typeof lands == 'object') {
              scope.filtered.lands = angular.copy(lands);
            }
          });

          scope.$watch('sites', function(sites) {
            if(typeof sites == 'object') {
              scope.filtered.sites = angular.copy(sites);
            }
          });

          scope.$watchGroup(['villages', 'lands', 'sites'], function() {
            scope._all = scope.getAll();
          });

          if($stateParams.filter) {
            scope.filter = JSON.parse($stateParams.filter);
          } else {
            scope.filter = {};
          }
          scope.$watch('filter', function(filter, prevFilter) {
            if(filter !== prevFilter) {
              $rootScope.$broadcast('mapaguarani.filterChanged', filter);
              scope.curPage = 0;
            }
          }, true);

          /*
           * Paging
           */
          scope.perPage = attrs.perPage || 10;
          scope.curPage = (parseInt($stateParams.page)-1) || 0;

          scope.pageCount = function() {
            if(scope.filtered[scope.content] && scope.filtered[scope.content].length)
              return Math.ceil(scope.filtered[scope.content].length/scope.perPage)-1;
            else if(scope.filter.text) {
              return Math.ceil(scope.filtered.all.length/scope.perPage)-1;
            } else {
              return 0;
            }
          };
          scope.nextPage = function() {
            if(scope.curPage < scope.pageCount())
              scope.curPage++;
          }
          scope.prevPage = function() {
            if(scope.curPage > 0)
              scope.curPage--;
          }
          scope.$watch('curPage', function(page, prevPage) {

            if(page !== prevPage)
              $rootScope.$broadcast('mapaguarani.pageChanged', page);

            $(element).scrollTop(0);
            $(element).parent().scrollTop(0);
            $(element).parent().parent().scrollTop(0);
            $(element).parent().parent().parent().scrollTop(0);
          });

        }
      }
    }
  ]);

  directives.factory('guaraniMapService', [
    '$rootScope',
    function($rootScope) {
      var map;
      var layers = [];

      var cluster;

      return {
        setMap: function(m) {
          map = m;
          return map;
        },
        getMap: function() {
          return map;
        },
        addLayer: function(layer) {
          layers.push(layer);
        },
        toggleLayer: function(layer) {

        },
        updateBounds: function() {
          if(map && map.contentLayer) {
            var bounds = map.contentLayer.getBounds();
            if(!_.isEmpty(bounds)) {
              map.fitBounds(bounds);
            }
          }
        },
        clusterSelection: function(ids, type) {
          cluster = {
            type: type,
            ids: ids.slice(0)
          };
          console.log('from service', cluster);
          // $rootScope.$broadcast('clusterSelectionUpdated', cluster);
        },
        getCluster: function() {
          return cluster;
        }
      }
    }
  ]);

  directives.directive('guaraniMap', [
    'GuaraniService',
    'guaraniMapService',
    '$rootScope',
    '$state',
    '$window',
    '$timeout',
    function(Guarani, Map, $rootScope, $state, $window, $timeout) {
      return {
        restrict: 'E',
        scope: {
          center: '=',
          zoom: '='
        },
        link: function(scope, element, attrs) {

          scope.center = scope.center || [-16.107747, -51.103348];
          scope.zoom = scope.zoom || 5;

          angular.element(element).append('<div id="' + attrs.id + '"></div>"').attr('id', '');

          var map = L.map(attrs.id, {
            center: scope.center,
            zoom: scope.zoom
          });

          Map.setMap(map);

          map.addLayer(gm_hybrid);

          var baselayers = {
            'Mapa Mapbox': mapbox_streets,
            'Satélite Mapbox': mapbox_satellite,
            'Híbrido Mapbox': mapbox_hybrid,
            'Mapa Google': gm_roadmap,
            'Híbrido Google': gm_hybrid,
            'Terreno Google': gm_terrain
          };

          var layersControl = new L.Control.Layers(baselayers, {});
          map.addControl(layersControl);

          var clusterClick = function(ev, type) {
            if(ev.data) {
              if(ev.data.id == 0) {
                if(map.getZoom() < 16) {
                  map.setView(ev.latlng, map.getZoom() + 1);
                }
                if(ev.data.src == 'smalls' || ev.data.src == 'mids' || map.getZoom() > 14) {
                  var cluster = {
                    type: type,
                    ids: ev.data.cdb_list.split(',')
                  };
                  // $rootScope.$apply(function() {
                  //   $rootScope.$broadcast('mapaguarani.clusterSelection', cluster);
                  // });
                  $state.go('home', {clustered: cluster});
                  // scope.$apply(function() {
                  //   Map.clusterSelection(ev.data.cdb_list.split(','), type);
                  // });
                }
              } else {
                $state.go(type, {id: ev.data.id});
              }
            }
          };

          /*
           * Init Lands layer
           */
          var default_host = $window.location.hostname;
          var landsLayer = L.tileLayer('http://' + default_host + ':4000/indigenousland/{z}/{x}/{y}.png', {
           zIndex: 2
          });
          var landsGridLayer = new L.UtfGrid('http://' + default_host + ':4000/indigenousland/{z}/{x}/{y}.grid.json?interactivity=id,name', {
           useJsonP: false
          });
          landsGridLayer.on('click', function(ev) {
            if(ev.data)
              $state.go('land', {id: ev.data.id});
          });
          map.addLayer(landsLayer);
          map.addLayer(landsGridLayer);

          /*
           * Init villages layer
           */

          Guarani.sqlTiles('cluster_indigenousvillage', {
            interactivity: ['id','cdb_list','src']
          }).then(function(token) {
            var villagesLayer = L.tileLayer('http://' + default_host + ':4000/api/' + token + '/{z}/{x}/{y}.png', {
              zIndex: 10
            });
            var villagesGridLayer = new L.UtfGrid('http://' + default_host + ':4000/api/' + token + '/{z}/{x}/{y}.grid.json', {
              useJsonP: false
            });
            villagesGridLayer.on('click', function(ev) {
              clusterClick(ev, 'village');
            });
            map.addLayer(villagesLayer);
            map.addLayer(villagesGridLayer);
          });

          /*
           * Init archaeological sites layer
           */

          Guarani.sqlTiles('cluster_archaeologicalplace', {
            interactivity: ['id','cdb_list','src']
          }).then(function(token) {
            var sitesLayer = L.tileLayer('http://' + default_host + ':4000/api/' + token + '/{z}/{x}/{y}.png', {
              zIndex: 10
            });
            var sitesGridLayer = new L.UtfGrid('http://' + default_host + ':4000/api/' + token + '/{z}/{x}/{y}.grid.json', {
              useJsonP: false
            });
            sitesGridLayer.on('click', function(ev) {
              clusterClick(ev, 'site');
            });
            map.addLayer(sitesLayer);
            map.addLayer(sitesGridLayer);
          });

          // var legendsControl = L.control({position: 'bottomright'});
          // legendsControl.onAdd = function(map) {
          //   var div = L.DomUtil.create('div', 'info legend');
          //   var tenure;
          //   div.innerHTML += '<p><strong>Terras indígenas</strong></p>';
          //   for (tenure in landTenures) {
          //     div.innerHTML += '<i style="background:' + landTenures[tenure].style.fillColor + '"></i>' + landTenures[tenure].name + '<br>';
          //   }
          //   return div;
          // };
          // legendsControl.addTo(map);
          //
          // map.on('overlayadd', function(eventLayer) {
          //   // Switch to the Population legend...
          //   if (eventLayer.name === 'Terras indígenas') {
          //     legendsControl.addTo(this);
          //   }
          // });
          // map.on('overlayremove', function(eventLayer) {
          //   if (eventLayer.name === 'Terras indígenas') {
          //     this.removeControl(legendsControl);
          //   }
          // });
        }
      }
    }
  ])

})(angular, L, _);
