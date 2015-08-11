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

  directives.directive('guaraniSidebar', [
    function() {
      return {
        restrict: 'E',
        scope: {
          villages: '=',
          lands: '=',
          defaultContent: '=',
          filtered: '='
        },
        templateUrl: '/static/views/sidebar.html',
        link: function(scope, element, attrs) {

          /*
           * Filters
           */

          scope.filtered = scope.filtered || {};

          scope.$watch('villages', function(villages) {
            if(typeof villages == 'object')
              scope.filtered.villages = angular.copy(scope.villages);
          });

          scope.$watch('lands', function(lands) {
            if(typeof lands == 'object')
              scope.filtered.lands = angular.copy(scope.lands);
          });

          scope.filter = {};
          scope.$watch('filter', function() {
            scope.curPage = 0;
          }, true);

          /*
           * Content type
           */
          scope.content = scope.defaultContent || 'villages';
          scope.setContent = function(content) {
            scope.content = content;
            scope.curPage = 0;
          };

          /*
           * Paging
           */
          scope.perPage = attrs.perPage || 10;
          scope.curPage = attrs.currentPage || 0;

          scope.pageCount = function() {
            if(scope.filtered[scope.content].features)
              return Math.ceil(scope.filtered[scope.content].features.length/scope.perPage)-1;
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

          scope.$watch('curPage', function() {
            $(element).scrollTop(0);
          });
        }
      }
    }
  ]);

  directives.directive('guaraniMap', [
    function() {
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
          scope.$watch('villages', _.debounce(function(villages) {
            if(villagesLayer) {
              markerLayer.removeLayer(villagesLayer);
              villagesLayer = null;
            }
            if(villages && villages.features && villages.features.length) {
              villagesLayer = L.geoJson(villages, {
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
              // layersControl.addOverlay(markerLayer, 'Aldeias Indígenas');
              map.fitBounds(villagesLayer.getBounds());
            }
          }, 500), true);
          map.addLayer(markerLayer);

          /*
           * Polygon layer setup
           */
          var landsLayer;
          scope.$watch('lands', function(lands) {
            if(landsLayer) {
              map.removeLayer(landsLayer);
              landsLayer = null;
            }
            if(lands && lands.features && lands.features.length) {
              landsLayer = L.geoJson(lands, {
                style: function(feature) {
                  var style = {};
                  var landTenure = landTenures[feature.properties.land_tenure];
                  if (landTenure) {
                    style = landTenure.style;
                  }
                  style.opacity = 0.8;
                  style.fillOpacity = 0.5;
                  style.weight = 2;
                  return style;
                },
                onEachFeature: function(feature, layer) {
                  var landTenure = landTenures[feature.properties.landTenure];
                  if (landTenure)
                    layer.bindPopup(landTenure.name);
                  else
                    layer.bindPopup(feature.properties.landTenure);
                }
              });
              // map.addLayer(landsLayer);
              // layersControl.addOverlay(landsLayer, 'Terras indígenas');
            }
          });

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
