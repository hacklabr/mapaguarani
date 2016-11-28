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
  var gm_roadmap = new L.gridLayer.googleMutant({type: 'roadmap'});
  var gm_terrain = new L.gridLayer.googleMutant({type: 'terrain'});
  var gm_hybrid = new L.gridLayer.googleMutant({type: 'hybrid'});
  var gm_satellite = new L.gridLayer.googleMutant({type: 'satellite'});

  var access_token = 'pk.eyJ1IjoiYnJ1bm9zbWFydGluIiwiYSI6IjM1MTAyYTJjMWQ3NmVmYTg0YzQ0ZWFjZTg0MDZiYzQ3In0.ThelegmeGkO5Vwd6KTu6xA';
  var mapbox_url = 'http://api.tiles.mapbox.com/v4/{mapid}/{z}/{x}/{y}.png?access_token={access_token}';
  var mapbox_satellite = L.tileLayer(mapbox_url, {mapid: 'mapbox.satellite', access_token: access_token});
  var mapbox_streets   = L.tileLayer(mapbox_url, {mapid: 'mapbox.streets', access_token: access_token});
  var mapbox_hybrid   = L.tileLayer(mapbox_url, {mapid: 'mapbox.streets-satellite', access_token: access_token});

  // Official layers
  var default_host = window.location.hostname;
  var protected_areas_tile = L.tileLayer('http://' + default_host + ':4000/protected_areas_baseprotectedarea/{z}/{x}/{y}.png', {});
  var boundaries_cities_tile = L.tileLayer('http://' + default_host + ':4000/boundaries_city/{z}/{x}/{y}.png', {
    zIndex: 40
  });
  var boundaries_states_tile = L.tileLayer('http://' + default_host + ':4000/boundaries_state/{z}/{x}/{y}.png', {});
  var boundaries_countries_tile = L.tileLayer('http://' + default_host + ':4000/boundaries_country/{z}/{x}/{y}.png', {});

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
    'user',
    function($rootScope, $stateParams, Guarani, Map, user) {
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

          // Set current user
          scope.user = user;

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
          scope.filtered.villages = [];
          scope.filtered.lands = [];
          scope.filtered.sites = [];
          scope._all = [];

          // Get every available content for "search all" results
          scope.getAll = function() {
            var all = [];
            if (scope.villages !== undefined)
                all = all.concat(angular.copy(scope.villages));
            if (scope.lands !== undefined)
                all = all.concat(angular.copy(scope.lands));
            if (scope.sites !== undefined)
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
            if(typeof lands == 'object')
              scope.filtered.lands = angular.copy(lands);
          });

          // Watch sites content changes for filterable collection
          scope.$watch('sites', function(sites) {
            if(typeof sites == 'object')
              scope.filtered.sites = angular.copy(sites);
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
            guarani_presence: {
              name: 'Presença Guarani',
              ref: 'presence',
              label: 'name',
              options: [
                {presence: true, name: 'Sim'},
                {presence: false, name: 'Não'}
              ]
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
//            prominent_subgroup: {
//              name: 'Subgrupo de destaque',
//              ref: 'id',
//              label: 'name',
//              options: Guarani.getUniq(scope.lands, 'prominent_subgroup', 'id')
//            },
            land_tenure: {
              name: 'Situação fundiária',
              ref: 'id',
              label: 'name',
              options: Guarani.getUniq(scope.lands, 'land_tenure', 'id')
            }
//            land_tenure_status: {
//              name: 'Situação da posse',
//              ref: 'id',
//              label: 'name',
//              options: Guarani.getUniq(scope.lands, 'land_tenure_status', 'id')
//            }
          };

          /*
           * Paging
           */
          scope.perPage = attrs.perPage || 10;
          scope.curPage = (parseInt($stateParams.page)-1) || 0;

          scope.pageCount = function() {
            if(scope.filtered[scope.content] && scope.filtered[scope.content].length) {
              return Math.ceil(scope.filtered[scope.content].length/scope.perPage)-1;
            } else if(scope.filter.text) {
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
          'item': '=',
        },
        templateUrl: '/static/views/partials/list-item.html',
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
    '$http',
    function(Guarani, Map, $rootScope, $state, $window, $http) {
      return {
        restrict: 'E',
        scope: {
          center: '=',
          zoom: '='
        },
        link: function(scope, element, attrs) {

          var center = scope.center || [-16.107747, -51.103348];
          var zoom = scope.zoom || 5;

          angular.element(element).append('<div id="' + attrs.id + '"></div>"').attr('id', '');

          var map = L.map(attrs.id, {
            center: center,
            zoom: zoom,
            zoomControl: false,
            attributionControl: false,
            preferCanvas: true
          });

          // Store map leaflet object on map service
          Map.setMap(map);

          // Add base layers
          map.addLayer(gm_satellite);
          var baselayers = {
            'Mapa Mapbox': mapbox_streets,
            'Satélite Mapbox': mapbox_satellite,
            'Híbrido Mapbox': mapbox_hybrid,
            'Mapa Google': gm_roadmap,
            'Híbrido Google': gm_hybrid,
            'Terreno Google': gm_terrain,
            'Satélite Google': gm_satellite
          };

          var official_layers = {
            'Áreas de proteção ambiental': protected_areas_tile,
            'Limites Municípios': boundaries_cities_tile,
            'Limites Estados': boundaries_states_tile,
            'Limites Países': boundaries_countries_tile
          };

          var layersControl = new L.Control.Layers(baselayers, official_layers, {'position': 'topleft'});
          map.addControl(layersControl);

          var zoomControl = new L.control.zoom({'position': 'topleft'});
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

          var markerClick = function(ev, type) {
              if(ev.target && ev.target.feature && ev.target.feature.id) {
                $state.go(type, {id: ev.target.feature.id, focus: false});
              }
          };

          // Start interactive layers object (lands, sites and villages)
          scope.interactiveLayers = {};

          /*
           * Init Lands layer
           */
          var default_host = $window.location.hostname;
          var landsLayer = L.tileLayer('http://' + default_host + ':4000/indigenousland/{z}/{x}/{y}.png', {
           zIndex: 10
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
              div.innerHTML += '<p><span class="bg-item" style="background-color:' + tenure_map['Em processo de desapropriação ou aquisição'] + ';"></span> Em processo de desapropriação ou aquisição</p>';
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
        var sites_promisse = $http.get('/api/arch_geojson/').then(function (response){
            var sites_geojson = response.data;
            var sitesPointsLayer = L.geoJSON(sites_geojson, {
                onEachFeature: function (feature, layer) {
                    layer.on('click', function(ev) {
                      markerClick(ev, 'site');
                    });
                },
                pointToLayer: function (feature, latlng) {
                    var marker = L.circleMarker(latlng, {
                        radius: 4,
                        fillColor: "#5CA2D1",
                        color: "#5CA2D1",
                        weight: 2,
                        opacity: 0.8,
                        fillOpacity: 0.8,
                    });
                    return marker
                }
            });
            var sitesLayer = L.markerClusterGroup({
                maxClusterRadius: 20,
                iconCreateFunction: function (cluster) {
                    var childCount = cluster.getChildCount();
                    var radius;
                    var class_sufix;
                    // If the ranges below changes, then village-marker-cluster-[big/md/sm]
                    // css class in _map.scss must change too
                    if (childCount >= 50) {
                        radius = 32;
                        class_sufix = 'big';
                    } else if (15 < childCount < 30) {
                        radius = 20;
                        class_sufix = 'md';
                    } else {
                        radius = 10;
                        class_sufix = 'sm';
                    }
                    return L.divIcon({html: '<div><span>' + childCount + '</span></div>',
                                      className: 'site-marker-cluster-' + class_sufix,
                                      iconSize: L.point(radius, radius)});
                },
            });
            sitesLayer.addLayer(sitesPointsLayer);
            var sitesLegend = L.control({'position': 'bottomright'});
            sitesLegend.onAdd = function(map) {
              var div = L.DomUtil.create('div', 'info legend sites');
              div.innerHTML += '<p><span class="point-item" style="background-color: #5CA2D1;"></span> <strong>Sítios arqueológicos</strong></p>';
              return div;
            };
            // Store interactive layer configuration object
            scope.interactiveLayers.sites = {
              tile: sitesLayer,
              legend: sitesLegend,
              active: true
            };
            sitesLayer.name = 'sites';

            // Add Layer to map
            map.addLayer(sitesLayer);
        });

           /*
           * Init villages layer
           */
            var villages_promisse = $http.get('/api/villages_geojson/').then(function (response){
                var villages_geojson = response.data;
                var villagesLayerMarkers = L.geoJSON(villages_geojson, {
                    onEachFeature: function (feature, layer) {
                        layer.on('click', function(ev) {
                          markerClick(ev, 'village');
                        });
                    },
                    pointToLayer: function (feature, latlng) {
                        // presence factor is 0, if no presence, or 1, if there is presence
                        var factor = 0;
                        if (feature.properties.guarani_presence.presence)
                            factor = 1;
                        var marker = L.circleMarker(latlng, {
                            radius: 4,
                            fillColor: "#e7ec13",
                            color: "#e7ec13",
                            weight: 2,
                            opacity: 0.8 * (1 - factor),
                            fillOpacity: 0.8 * factor,
                        });
                        return marker
                    }
                });
                // var villagesLayer = L.vectorGrid.slicer(villages_geojson);
                // map.addLayer(villagesLayer);
                var villagesLayer = L.markerClusterGroup({
                    maxClusterRadius: 20,
                    iconCreateFunction: function (cluster) {
                        var childCount = cluster.getChildCount();
                        var radius;
                        var class_sufix;
                        // If the ranges below changes, then village-marker-cluster-[big/md/sm]
                        // css class in _map.scss must change too
                        if (childCount >= 50) {
                            radius = 32;
                            class_sufix = 'big';
                        } else if (15 < childCount < 30) {
                            radius = 20;
                            class_sufix = 'md';
                        } else {
                            radius = 10;
                            class_sufix = 'sm';
                        }
                        return L.divIcon({html: '<div><span>' + childCount + '</span></div>',
                                          className: 'village-marker-cluster-' + class_sufix,
                                          iconSize: L.point(radius, radius)});
                    },
                });
                villagesLayer.addLayer(villagesLayerMarkers);

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
                  legend: villagesLegend,
                  active: true
                };
                villagesLayer.name = 'villages';

                // Add Layer to map
                map.addLayer(villagesLayer);

                var show_label_zoom = 11; // zoom level threshold for showing/hiding labels
                var labels_visible = false;

                map.on('zoomend', function (e) {
                    var cur_zoom = map.getZoom();
                    if (labels_visible && cur_zoom < show_label_zoom) {
                        labels_visible = false;
                        villagesLayerMarkers.eachLayer(function (layer) {
                            // Show label
                            layer.unbindTooltip();
                        });
                    } else if(!labels_visible && cur_zoom >= show_label_zoom) {
                        labels_visible = true;
                        villagesLayerMarkers.eachLayer(function (layer) {
                            // Show label
                            layer.bindTooltip(layer.feature.properties.name, {
                                permanent: true,
                                direction: 'bottom',
                                opacity: 0.7,
                            });
                        });
                    }
                });
            });

          // Watch layer toggle to hide/display layer on leaflet
          $rootScope.$on('mapaguarani.toggleLayer', function(ev, layer) {
              if(scope.interactiveLayers[layer]) {
                if(scope.interactiveLayers[layer].active) {
                  scope.interactiveLayers[layer].active = false;
                  map.removeLayer(scope.interactiveLayers[layer].tile);
                  if (layer === 'lands')
                    map.removeLayer(scope.interactiveLayers[layer].grid);
                } else {
                  scope.interactiveLayers[layer].active = true;
                  map.addLayer(scope.interactiveLayers[layer].tile);
                  if (layer === 'lands')
                    map.addLayer(scope.interactiveLayers[layer].grid);
                }
              }
          });

          // Control legend map display according to device display Width ($window.innerWidth)
          if ($window.innerWidth < 800) {
              scope.display_legends = false;
              $rootScope.menuIsClosed = true;
              map.removeControl(scope.interactiveLayers.lands.legend);
          } else {
              scope.display_legends = true;
          }

          villages_promisse.then(function (){
              if (!scope.display_legends)
                map.removeControl(scope.interactiveLayers.villages.legend);
          })

          sites_promisse.then(function (){
              if (!scope.display_legends)
                map.removeControl(scope.interactiveLayers.sites.legend);
          })

          angular.element($window).bind('resize', function () {
            if (!scope.display_legends && $window.innerWidth >= 800) {
                scope.display_legends = true;
                map.addControl(scope.interactiveLayers.villages.legend);
                map.addControl(scope.interactiveLayers.sites.legend);
                map.addControl(scope.interactiveLayers.lands.legend);
            } else if (scope.display_legends && $window.innerWidth < 800) {
                scope.display_legends = false;
                map.removeControl(scope.interactiveLayers.villages.legend);
                map.removeControl(scope.interactiveLayers.sites.legend);
                map.removeControl(scope.interactiveLayers.lands.legend);
            }
          });
        }
      }
    }
  ])

})(angular, L, _);
