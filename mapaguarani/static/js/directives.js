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

  var landTenures = {
    'no_arrangements': {
      name: 'Sem Providências',
      style: {
        color: '#ffffff',
        fillColor: '#ffffff',
        dashArray: '5'
      }
    },
    'regularized': {
      name: 'Regularizada',
      style: {
        color: '#009933',
        fillColor: '#33AD5C'
      }
    },
    'expropriated': {
      name: 'Desapropriada',
      style: {
        color: '#00E600',
        fillColor: '#00FF00',
        dashArray: '5'
      }
    },
    'expropriated_in_progress': {
      name: 'Em processo de desapropriação',
      style: {
        color: '#4DFF4D',
        fillColor: '#66FF66',
        dashArray: '5'
      }
    },
    'delimited': {
      name: 'Delimitada',
      style: {
        color: '#00FF99',
        fillColor: '#33FFAD',
        dashArray: '5'
      }
    },
    'study': {
      name: 'Em estudo',
      style: {
        color: '#FF3300',
        fillColor: '#FF4719',
        dashArray: '5'
      }
    },
    'declared': {
      name: 'Declarada',
      style: {
        color: '#CC9900',
        fillColor: '#D6AD33'
      }
    },
    'acquired': {
      name: 'Adquirida',
      style: {
        color: '#CC9900',
        fillColor: '#D6AD33'
      }
    },
    'regularized_limits_rev': {
      name: 'Regularizada (Em revisão de limites)',
      style: {
        color: '#EBD699',
        fillColor: '#F5EBCC'
      }
    }
  };

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
            disableClusteringAtZoom: 8 // 8 para Google Maps
          });

          /*
           * Marker layer setup
           */
          var villagesLayer;
          scope.$watch('villages', function(villages) {
            if(villagesLayer) {
              markerLayer.removeLayer(villagesLayer);
              markerLayer = null;
            }
            if(villages) {
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
              layersControl.addOverlay(markerLayer, 'Aldeias Indígenas');
            }
          });
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
            if(lands) {
              landsLayer = L.geoJson(lands, {
                style: function(feature) {
                  var style = {};
                  var landTenure = landTenures[feature.properties.landTenure];
                  if (landTenure) {
                    style = landTenure.style;
                  }
                  style.opacity = 0.8;
                  style.fillOpacity = 0.5;
                  style.weight = 2
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
              map.addLayer(landsLayer);
              layersControl.addOverlay(landsLayer, 'Terras indígenas');
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
