(function(angular, L, _) {
  'use strict';

  var directives = angular.module('mapaguarani.directives', []);

  /*
   * Lock sidebar height to proper site grid limits
   */
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

  /*
   * Store map layers
   */
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

  /*
   * Loading message
   */
  directives.directive('loading', [
    '$rootScope',
    function($rootScope) {
      return {
        restrict: 'A',
        link: function(scope, element, attrs) {
          $rootScope.$on('mapaguarani.loaded', function() {
            angular.element(element).remove();
          });
        }
      }
    }
  ])

  /*
   * Sidebar list directive
   * Display and filter items
   */
  directives.directive('guaraniList', [
    '$rootScope',
    '$stateParams',
    'GuaraniService',
    'guaraniMapService',
    function($rootScope, $stateParams, Guarani, Map) {
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
          // Watch content to broacast change of value and clear filters
          scope.$watch('content', function(content, prevContent) {
            if(content !== prevContent) {
              $rootScope.$broadcast('mapaguarani.contentChanged', content);
              scope.filter.advanced = undefined;
              scope.showAdv = false;
            }
          });

          /*
           * Layer toggler
           */
          // Available layers, all enabled by default
          scope.activeLayers = {
            'villages': true,
            'lands': true,
            'sites': true
          };
          // Toggler
          scope.toggleLayer = function(layer) {
            if(scope.activeLayers[layer])
              scope.activeLayers[layer] = false;
            else
              scope.activeLayers[layer] = true;
            Map.toggleLayer(layer);
          };

          /*
           * Filters
           */
          scope.filtered = scope.filtered || {};

          // Get every available content for "search all" results
          scope.getAll = function() {
            var all = [];
            all = all.concat(angular.copy(scope.villages));
            all = all.concat(angular.copy(scope.lands));
            all = all.concat(angular.copy(scope.sites));
            return all;
          };

          // Watch village content changes for filterable collection
          scope.$watch('villages', function(villages) {
            if(typeof villages == 'object')
              scope.filtered.villages = angular.copy(villages);
          });

          // Watch lands content changes for filterable collection
          scope.$watch('lands', function(lands) {
            if(typeof lands == 'object') {
              scope.filtered.lands = angular.copy(lands);
            }
          });

          // Watch sites content changes for filterable collection
          scope.$watch('sites', function(sites) {
            if(typeof sites == 'object') {
              scope.filtered.sites = angular.copy(sites);
            }
          });

          // Watch all content changes to store `getAll` on scope
          scope.$watchGroup(['villages', 'lands', 'sites'], function() {
            scope._all = scope.getAll();
          });

          // Use state params defined filters
          if($stateParams.filter) {
            scope.filter = JSON.parse($stateParams.filter);
          } else {
            scope.filter = {};
          }
          // Watch filter changes to broadcast and reset paging
          scope.$watch('filter', function(filter, prevFilter) {
            if(filter !== prevFilter) {
              $rootScope.$broadcast('mapaguarani.filterChanged', filter);
              scope.curPage = 0;
            }
          }, true);

          /*
           * Advanced filters
           */

          scope.showAdv = scope.filter.advanced ? true : false;
          scope.toggleAdv = function() {
            if(scope.showAdv) {
              scope.showAdv = false;
              scope.filter.advanced = undefined;
            } else
              scope.showAdv = true;
          };

          /*
           * Config adv nav fields for each content type
           */
          scope.adv = {};
          scope.adv.villages = {
            ethnic_groups: {
              name: 'Grupos étnicos',
              ref: 'id',
              label: 'name',
              options: Guarani.getUniq(scope.villages, 'ethnic_groups', 'id')
            },
            prominent_subgroup: {
              name: 'Subgrupo de destaque',
              ref: 'id',
              label: 'name',
              options: Guarani.getUniq(scope.villages, 'prominent_subgroup', 'id')
            }
          };
          scope.adv.lands = {
            ethnic_groups: {
              name: 'Grupos étnicos',
              ref: 'id',
              label: 'name',
              options: Guarani.getUniq(scope.lands, 'ethnic_groups', 'id')
            },
            prominent_subgroup: {
              name: 'Subgrupo de destaque',
              ref: 'id',
              label: 'name',
              options: Guarani.getUniq(scope.lands, 'prominent_subgroup', 'id')
            },
            land_tenure: {
              name: 'Posse',
              ref: 'id',
              label: 'name',
              options: Guarani.getUniq(scope.lands, 'land_tenure', 'id')
            },
            land_tenure_status: {
              name: 'Situação da posse',
              ref: 'id',
              label: 'name',
              options: Guarani.getUniq(scope.lands, 'land_tenure_status', 'id')
            }
          };

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

  /*
   * Single item directive
   */
  directives.directive('guaraniItem', [
    '$state',
    function($state) {
      return {
        restrict: 'EA',
        scope: {
          'item': '='
        },
        templateUrl: '/static/views/partials/list-item.html',
        link: function(scope, element, attrs) {

          // Identify content type from item layer name
          var type;
          switch(scope.item.layer.name) {
            case 'Aldeias Indígenas':
              type = 'village';
              break;
            case 'Terras Indígenas':
              type = 'land';
              break;
            case 'Sítios Arqueológicos':
              type = 'site';
              break;
          }

          // Get item url
          scope.url = $state.href(type, {id: scope.item.id}, {inherit: false});

        }
      }
    }
  ]);

  /*
   * Map interaction service
   */
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
          $rootScope.$broadcast('mapaguarani.toggleLayer', layer);
        },
        updateBounds: function() {
          if(map) {
            map.setView([-16.107747, -51.103348], 5);
          }
        }
      }
    }
  ]);

  /*
   * Map directive
   */
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
            zoom: scope.zoom,
            zoomControl: false
          });

          // Store map leaflet object on map service
          Map.setMap(map);

          // Add base layers
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

          var zoomControl = new L.control.zoom({'position': 'topright'});
          map.addControl(zoomControl);
          L.control.scale({'position':'bottomright','imperial':false }).addTo(map);;
          // Watch layer toggling to display legends
          map.on('layeradd', function(ev) {
            if(ev.layer.name && scope.interactiveLayers[ev.layer.name])
              map.addControl(scope.interactiveLayers[ev.layer.name].legend);
          });
          map.on('layerremove', function(ev) {
            if(ev.layer.name && scope.interactiveLayers[ev.layer.name])
              map.removeControl(scope.interactiveLayers[ev.layer.name].legend);
          });

          // Cluster click callback
          var clusterClick = function(ev, type) {
            if(ev.data) {
              if(ev.data.id == 0) {
                // if(map.getZoom() < 16) {
                  map.setView(ev.latlng, map.getZoom() + 1);
                  // map.zoomIn();
                  map.invalidateSize(true);
                // }
                // if(ev.data.src == 'smalls' || map.getZoom() > 14) {
                //   var cluster = {
                //     type: type,
                //     ids: _.map(ev.data.cdb_list.split(','), function(id) { return parseInt(id); })
                //   };
                //   $state.go('home', {clustered: JSON.stringify(cluster)});
                // }
              } else {
                $state.go(type, {id: ev.data.id, focus: false});
              }
            }
          };

          // Start interactive layers object (lands, sites and villages)
          scope.interactiveLayers = {};

          /*
           * Init Lands layer
           */
          var default_host = $window.location.hostname;
          var landsLayer = L.tileLayer('http://' + default_host + ':4000/indigenousland/{z}/{x}/{y}.png', {
           zIndex: 3
          });
          var landsGridLayer = new L.UtfGrid('http://' + default_host + ':4000/indigenousland/{z}/{x}/{y}.grid.json?interactivity=id,name', {
           useJsonP: false
          });
          landsGridLayer.on('click', function(ev) {
            if(ev.data)
              $state.go('land', {id: ev.data.id, focus: false});
          });
          var landsLegend = L.control({'position': 'bottomright'});
          landsLegend.onAdd = function(map) {
            var div = L.DomUtil.create('div', 'info legend lands');
            div.innerHTML += '<p><strong>Terras indígenas</strong></p>';
            Guarani.tenures.query(function(tenures) {
              var tenure_map = {};
              _.each(tenures, function(tenure) {
                tenure_map[tenure.name] = tenure.map_color
              });
              div.innerHTML += '<p><span class="bg-item" style="background-color:' + tenure_map['Sem providências'] + ';"></span> Sem providências</p>';
              div.innerHTML += '<p><span class="bg-item" style="background-color:' + tenure_map['Em estudo'] + ';"></span> Em estudo</p>';
              div.innerHTML += '<p><span class="bg-item" style="background-color:' + tenure_map['Delimitada'] + ';"></span> Delimitada</p>';
              div.innerHTML += '<p><span class="bg-item" style="background-color:' + tenure_map['Declarada'] + ';"></span> Declarada</p>';
              div.innerHTML += '<p><span class="bg-item" style="background-color:' + tenure_map['Homologada'] + ';"></span> Homologada ou Regularizada</p>';
              div.innerHTML += '<p class="divider"></p>';
              div.innerHTML += '<p><span class="bg-item" style="background-color:' + tenure_map['Em processo de desapropriação'] + ';"></span> Em processo de desapropriação ou aquisição</p>';
              div.innerHTML += '<p><span class="bg-item" style="background-color:' + tenure_map['Adquirida'] + ';"></span> Desapropriada ou Adquirida</p>';

              div.innerHTML += '<p class="divider"></p>' +
              '<p><span class="point-item legend1"></span> delimitadas, declaradas, homologadas ou desapropriadas/adquiridas</p>' +
              '<p><span class="point-item legend2"></span> em reestudo</p>' +
              '<p><span class="point-item legend3"></span> não delimitadas</p>';
            });
//            Guarani.tenures_status.query(function(tenures) {
//              _.each(tenures, function(tenure) {
//                div.innerHTML += '<p><span class="border-item" style="border-color:' + tenure.map_color + ';"></span> ' + tenure.name + '</p>';
//              });
//            });
            return div;
          };
          // Store interactive layer configuration object
          scope.interactiveLayers.lands = {
            tile: landsLayer,
            grid: landsGridLayer,
            legend: landsLegend,
            active: true
          };
          landsLayer.name = 'lands';
          map.addLayer(landsLayer);
          map.addLayer(landsGridLayer);

          /*
           * Init archaeological sites layer
           */

          Guarani.sqlTiles('cluster_archaeologicalplace', {
            interactivity: ['id','cdb_list','src']
          }).then(function(token) {
            var sitesLayer = L.tileLayer('http://' + default_host + ':4000/api/' + token + '/{z}/{x}/{y}.png', {
              zIndex: 4
            });
            var sitesGridLayer = new L.UtfGrid('http://' + default_host + ':4000/api/' + token + '/{z}/{x}/{y}.grid.json', {
              useJsonP: false
            });
            sitesGridLayer.on('click', function(ev) {
              clusterClick(ev, 'site');
            });
            var sitesLegend = L.control({'position': 'bottomright'});
            sitesLegend.onAdd = function(map) {
              var div = L.DomUtil.create('div', 'info legend sites');
              div.innerHTML += '<p><span class="point-item" style="background-color: #5CA2D1;"></span> <strong>Sítios arqueológicos</strong></p>';
              return div;
            };
            // Store interactive layer configuration object
            scope.interactiveLayers.sites = {
              tile: sitesLayer,
              grid: sitesGridLayer,
              legend: sitesLegend,
              active: true
            };
            sitesLayer.name = 'sites';
            map.addLayer(sitesLayer);
            map.addLayer(sitesGridLayer);
          });

          /*
           * Init villages layer
           */

          Guarani.sqlTiles('cluster_indigenousvillage', {
            interactivity: ['id','cdb_list','src', 'presence']
          }).then(function(token) {
            var villagesLayer = L.tileLayer('http://' + default_host + ':4000/api/' + token + '/{z}/{x}/{y}.png', {
              zIndex: 5
            });
            var villagesGridLayer = new L.UtfGrid('http://' + default_host + ':4000/api/' + token + '/{z}/{x}/{y}.grid.json', {
              useJsonP: false
            });
            villagesGridLayer.on('click', function(ev) {
              clusterClick(ev, 'village');
            });
            var villagesLegend = L.control({'position': 'bottomright'});
            villagesLegend.onAdd = function(map) {
              var div = L.DomUtil.create('div', 'info legend villages');
              div.innerHTML += '<p><strong>Aldeias Indígenas</strong></p>' +
              '<p><span class="point-item legend2"></span> antigas áreas de uso ou áreas esbulhadas</p>' +
              '<p><span class="point-item legend1"></span> habitadas atualmente</p>';
              return div;
            };
            // Store interactive layer configuration object
            scope.interactiveLayers.villages = {
              tile: villagesLayer,
              grid: villagesGridLayer,
              legend: villagesLegend,
              active: true
            };
            villagesLayer.name = 'villages';
            map.addLayer(villagesLayer);
            map.addLayer(villagesGridLayer);
          });

          // Watch layer toggle to hide/display layer on leaflet
          $rootScope.$on('mapaguarani.toggleLayer', function(ev, layer) {
              if(scope.interactiveLayers[layer]) {
                if(scope.interactiveLayers[layer].active) {
                  scope.interactiveLayers[layer].active = false;
                  map.removeLayer(scope.interactiveLayers[layer].tile);
                  map.removeLayer(scope.interactiveLayers[layer].grid);
                } else {
                  scope.interactiveLayers[layer].active = true;
                  map.addLayer(scope.interactiveLayers[layer].tile);
                  map.addLayer(scope.interactiveLayers[layer].grid);
                }

              }
          });
        }
      }
    }
  ])

})(angular, L, _);
