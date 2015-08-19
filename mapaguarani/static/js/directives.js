(function(angular) {
  'use strict';

  var directives = angular.module('mapaguarani.directives', []);

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

  var landTenures = window.landTenures;

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
          scope.content = $stateParams.content || 'villages';
          scope.setContent = function(content) {
            scope.content = content;
            scope.curPage = 0;
          };
          scope.$watch('content', function(content, prevContent) {
            if(content !== prevContent)
              $rootScope.$broadcast('mapaguarani.contentChanged', content);
          });

          /*
           * Filters
           */
          scope.filtered = scope.filtered || {};

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
            else
              return 0;
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
          });
        }
      }
    }
  ]);

  directives.factory('guaraniMapService', [
    function() {
      var map, data;
      return {
        setMap: function(m) {
          map = m;
          return map;
        },
        getMap: function() {
          return map;
        },
        setData: function(d) {
          data = d;
          return data;
        },
        getData: function() {
          return data;
        }
      }
    }
  ]);

  directives.directive('guaraniMap', [
    'GuaraniService',
    'guaraniMapService',
    function(Guarani, Map) {
      return {
        restrict: 'E',
        scope: {
          center: '=',
          zoom: '=',
          villages: '=',
          lands: '='
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

          var data;
          scope.$watch(function() {
            return Map.getData();
          }, function(d) {
            data = d;
          });

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

          var markerLayer = L.markerClusterGroup({
            maxClusterRadius: 28,
            // disableClusteringAtZoom: 8 // 8 para Google Maps
          });

          /*
           * Marker layer setup
           */
          var villagesLayer;
          var villageIcon = L.divIcon({className: 'village-marker'});
          scope.$watch('villages', _.debounce(function(villages) {
            if(villagesLayer) {
              markerLayer.removeLayer(villagesLayer);
              villagesLayer = null;
            }
            if(villages && villages.length) {
              villagesLayer = L.geoJson(Guarani.toGeoJSON(villages), {
                pointToLayer: function(feature, latlng) {
                  return L.marker(latlng, {icon: villageIcon});
                },
                onEachFeature: function(feature, layer) {
                  var popupOptions = {maxWidth: 200};
                  layer.bindPopup("<b>Aldeia: </b> " + feature.properties.name +
                  "<br><b>Outros nomes: </b>" + feature.properties.other_names +
                  "<br><b>Grupo étnico: </b>" + feature.properties.ethnic_groups2 +
                  "<br><b>População: </b>" + feature.properties.population +
                  "<br><b>Presença guarani: </b>" + feature.properties.guarani_presence
                  ,popupOptions);
                }
              });
              markerLayer.addLayer(villagesLayer);
              map.fitBounds(villagesLayer.getBounds());
            }
          }, 700), true);
          map.addLayer(markerLayer);
          layersControl.addOverlay(markerLayer, 'Aldeias Indígenas');

          /*
           * Polygon layer setup
           */
          var landsLayer;
          scope.$watch('lands', _.debounce(function(lands) {
            if(landsLayer) {
              layersControl.removeLayer(landsLayer);
              map.removeLayer(landsLayer);
              landsLayer = null;
            }
            if(lands && lands.length) {
              landsLayer = L.geoJson(Guarani.toGeoJSON(lands), {
                style: function(feature) {
                  var style = {};

                  if(feature.properties.land_tenure_status)
                    style.color = feature.properties.land_tenure_status.map_color;
                  if(feature.properties.land_tenure)
                    style.fillColor = feature.properties.land_tenure.map_color;

                  style.opacity = 0.8;
                  style.fillOpacity = 0.5;
                  style.weight = 2;
                  return style;
                },
                onEachFeature: function(feature, layer) {
                  layer.bindPopup(feature.properties.name);
                }
              });
              map.addLayer(landsLayer);
              map.fitBounds(landsLayer.getBounds());
              layersControl.addOverlay(landsLayer, 'Terras indígenas');
            }
          }, 700), true);

          var legendsControl = L.control({position: 'bottomright'});
          legendsControl.onAdd = function(map) {
            var div = L.DomUtil.create('div', 'info legend');
            var tenure;
            div.innerHTML += '<p><strong>Terras indígenas</strong></p>';
            for (tenure in landTenures) {
              div.innerHTML += '<i style="background:' + landTenures[tenure].style.fillColor + '"></i>' + landTenures[tenure].name + '<br>';
            }
            return div;
          };
          legendsControl.addTo(map);

          map.on('overlayadd', function(eventLayer) {
            // Switch to the Population legend...
            if (eventLayer.name === 'Terras indígenas') {
              legendControl.addTo(this);
            }
          });
          map.on('overlayremove', function(eventLayer) {
            if (eventLayer.name === 'Terras indígenas') {
              this.removeControl(legendsControl);
            }
          });
        }
      }
    }
  ])

})(angular);
