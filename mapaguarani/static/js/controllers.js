(function(angular){
    'use strict';

    var mapaguarani_controllers = angular.module('mapaguarani.controllers', []);

    mapaguarani_controllers.controller('GuaraniMapCtrl', ['$scope',
        'IndigenousVillage',
        'IndigenousLands',
        function ($scope, IndigenousVillage, IndigenousLands) {

            var map = L.map('map', {
                center: [-23.5408, -46.6400],
                zoom: 5
                //layers: [grayscale, cities]
            });

            var gm_roadmap = new L.Google('ROADMAP');
            var gm_terrain = new L.Google('TERRAIN');
            var gm_hybrid = new L.Google('HYBRID');
            var baselayers = {
                'Mapa': gm_roadmap,
                'Hibrido': gm_hybrid,
                'Terreno': gm_terrain
            };
            map.addLayer(gm_roadmap);

            map.addControl(new L.Control.Layers( baselayers, {}));

            //angular.extend($scope, {
            //    center: {
            //        lat: -23.5408,
            //        lng: -46.6400,
            //        zoom: 5
            //    },
            //    layers: {
            //        baselayers: {
            //            googleTerrain: {
            //                name: 'Terreno',
            //                layerType: 'TERRAIN',
            //                type: 'google'
            //            },
            //            googleHybrid: {
            //                name: 'Hybrido',
            //                layerType: 'HYBRID',
            //                type: 'google'
            //            },
            //            googleRoadmap: {
            //                name: 'Mapa',
            //                layerType: 'ROADMAP',
            //                type: 'google'
            //            }
            //        }
            //    },
            //    defaults: {
            //        scrollWheelZoom: true
            //    }
            //});

            IndigenousVillage.get({}, function(villages){

                var markers = L.markerClusterGroup({
                    maxClusterRadius: 30,
                    disableClusteringAtZoom :8
                });
                var geoJsonLayer = L.geoJson(villages, {
                    onEachFeature: function (feature, layer) {
                        var popupOptions = {maxWidth: 200};
                        layer.bindPopup("<b>Aldeia: </b> " + feature.properties.name +
                                        "<br><b>Outros nomes: </b>" + feature.properties.other_names +
                                        "<br><b>Grupo étnico: </b>" + feature.properties.ethnic_groups2 +
                                        "<br><b>População: </b>" + feature.properties.population +
                                        "<br><b>Presença guarani: </b>" + feature.properties.guarani_presence
                            ,popupOptions);
                    }
                });
                markers.addLayer(geoJsonLayer);
                map.addLayer(markers);
            });

            IndigenousLands.get({}, function(lands){
                L.geoJson(lands, {
                    //style: function (feature) {
                    //    return {color: feature.properties.color};
                    //},
                    //onEachFeature: function (feature, layer) {
                    //    layer.bindPopup(feature.properties.description);
                    //}
                }).addTo(map);
            });
        }
    ]);
})(angular);