(function(angular, L, _) {
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
        },
        updateBounds: function() {
          if(map && map.contentLayer) {
            var bounds = map.contentLayer.getBounds();
            if(!_.isEmpty(bounds)) {
              map.fitBounds(bounds);
            }
          }
        }
      }
    }
  ]);

  directives.directive('guaraniMap', [
    'GuaraniService',
    'guaraniMapService',
    '$rootScope',
    '$state',
    function(Guarani, Map, $rootScope, $state) {
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

          var contentLayer = new L.FeatureGroup();
          map.addLayer(contentLayer);
          map.contentLayer = contentLayer;

          /*
           * Marker layer setup
           */

          /*
           * Init Lands layer
           */
          var landsLayer = new L.FeatureGroup();
          contentLayer.addLayer(landsLayer);

          /*
           * Init Villages layer
           */
          var villagesLayer = new L.MarkerClusterGroup({
            maxClusterRadius: 25,
            iconCreateFunction: function(cluster) {
              return new L.DivIcon({ html: '<div><span>' + cluster.getChildCount() + '</span></div>', className: 'villages-cluster marker-cluster', iconSize: new L.Point(40, 40) });
            }
          });
          contentLayer.addLayer(villagesLayer);
          var villageGuaraniIcon = L.divIcon({className: 'village-guarani-marker'});
          var villageOtherIcon = L.divIcon({className: 'village-other-marker'});

          /*
           * Init sites layer
           */
          var sitesLayer = new L.MarkerClusterGroup({
            maxClusterRadius: 25,
            iconCreateFunction: function(cluster) {
              return new L.DivIcon({ html: '<div><span>' + cluster.getChildCount() + '</span></div>', className: 'sites-cluster marker-cluster', iconSize: new L.Point(40, 40) });
            }
          });
          contentLayer.addLayer(sitesLayer);
          var sitesIcon = L.divIcon({className: 'site-marker'});

          var landsLayer = L.tileLayer('http://localhost:4000/indigenousland/{z}/{x}/{y}.png');
          var landsGridLayer = new L.UtfGrid('http://localhost:4000/indigenousland/{z}/{x}/{y}.grid.json?interactivity=id,name', {
            useJsonP: false
          });
          map.addLayer(landsLayer);
          map.addLayer(landsGridLayer);

          var villagesMarker = [];
          var villagesTileLayer = new L.TileLayer.GeoJSON('/tiles/villages/{z}/{x}/{y}.geojson', {
            clipTiles: true,
            layer: villagesLayer,
            unique: function(feature) {
              return feature.id;
            }
          }, {
            pointToLayer: function(feature, latlng) {
              var icon = villageGuaraniIcon;
              if(feature.properties.ethnic_groups && feature.properties.ethnic_groups.length > 1)
                icon = villageOtherIcon;
              var marker = new L.Marker(latlng, {icon: icon});
              villagesLayer.addLayer(marker);
              villagesMarker.push(marker);
              marker.on('click', function() {
                $rootScope.$apply(function() {
                  // $state.go('home.village', { id: feature.id });
                });
              });
              return null;
            }
          });
          villagesLayer.addLayer(villagesTileLayer);
          map.on('zoomstart', function() {
            villagesMarker.forEach(function(marker) {
              villagesLayer.removeLayer(marker);
            });
          });

          var sitesMarker = [];
          var sitesTileLayer = new L.TileLayer.GeoJSON('/tiles/archaeological/{z}/{x}/{y}.geojson', {
            clipTiles: true,
            unique: function(feature) {
              return feature.id;
            }
          }, {
            pointToLayer: function(feature, latlng) {
              var icon = sitesIcon;
              var marker = new L.Marker(latlng, {icon: icon});
              sitesLayer.addLayer(marker);
              sitesMarker.push(marker);
              marker.on('click', function() {
                $rootScope.$apply(function() {
                  // $state.go('home.site', { id: feature.id });
                });
              });
              return null;
            }
          });
          sitesLayer.addLayer(sitesTileLayer);
          map.on('zoomstart', function() {
            sitesMarker.forEach(function(marker) {
              sitesLayer.removeLayer(marker);
            });
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
