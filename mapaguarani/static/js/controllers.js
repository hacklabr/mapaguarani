(function(angular){
    'use strict';

    var mapaguarani_controllers = angular.module('mapaguarani.controllers', []);

    mapaguarani_controllers.controller('GuaraniMapCtrl', ['$scope',
        'IndigenousVillage',
        'IndigenousLands',
        function ($scope, IndigenousVillage, IndigenousLands) {

            var map = L.map('map', {
                center: [-16.107747, -51.103348],
                zoom: 5
            });

            //Google maps - leaflet 0.7 only
            var gm_roadmap = new L.Google('ROADMAP');
            var gm_terrain = new L.Google('TERRAIN');
            var gm_hybrid = new L.Google('HYBRID');
            map.addLayer(gm_hybrid);

            // Mapbox - leaflet 1.0 compatible
            var access_token = 'pk.eyJ1IjoiYnJ1bm9zbWFydGluIiwiYSI6IjM1MTAyYTJjMWQ3NmVmYTg0YzQ0ZWFjZTg0MDZiYzQ3In0.ThelegmeGkO5Vwd6KTu6xA'
            var mapbox_url = 'http://api.tiles.mapbox.com/v4/{mapid}/{z}/{x}/{y}.png?access_token={access_token}'
            var mapbox_satalite = L.tileLayer(mapbox_url, {mapid: 'mapbox.satellite', access_token: access_token}),
                mapbox_streets   = L.tileLayer(mapbox_url, {mapid: 'mapbox.streets', access_token: access_token}),
                mapbox_hybrid   = L.tileLayer(mapbox_url, {mapid: 'mapbox.streets-satellite', access_token: access_token});

            var baselayers = {
                'Mapa Mapbox': mapbox_streets,
                'Satélite Mapbox': mapbox_satalite,
                'Híbrido Mapbox': mapbox_hybrid,
                'Mapa Google': gm_roadmap,
                'Híbrido Google': gm_hybrid,
                'Terreno Google': gm_terrain
            };
            //map.addLayer(mapbox_satalite);
            // end Mapbox

            var layers_control = new L.Control.Layers( baselayers, {})
            map.addControl(layers_control);

            IndigenousVillage.get({}, function(villages){

                var villages_layer = L.geoJson(villages, {
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
                //map.addLayer(villages_layer);
                //layers_control.addOverlay(villages_layer, 'Aldeias Indígenas');

                var markers = L.markerClusterGroup({
                    maxClusterRadius: 28,
                    //disableClusteringAtZoom : 7
                    disableClusteringAtZoom : 8 // 8 para Googlemaps
                });
                markers.addLayer(villages_layer);
                map.addLayer(markers);
                layers_control.addOverlay(markers, 'Aldeias Indígenas');
            });

            var land_tenures = {
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

            var legend_control = L.control({position: 'bottomright'});
            legend_control.onAdd = function (map) {
                var div = L.DomUtil.create('div', 'info legend');
                var tenure;
                div.innerHTML += '<p><strong>Terras indígenas</strong></p>';
                for (tenure in land_tenures) {
                    div.innerHTML +=
                        '<i style="background:' + land_tenures[tenure].style.fillColor + '"></i> ' +
                        land_tenures[tenure].name + '<br>';
                }
                return div;
            };

            IndigenousLands.get({}, function(lands){
                var indigenous_lands_layer = L.geoJson(lands, {
                    style: function (feature) {
                        var style = {};
                        var land_tenure = land_tenures[feature.properties.land_tenure];
                        if (land_tenure) {
                            style = land_tenure.style;
                        }
                        style.opacity = 0.8;
                        style.fillOpacity = 0.5;
                        style.weight = 2
                        return style;
                    },
                    onEachFeature: function (feature, layer) {
                        var land_tenure = land_tenures[feature.properties.land_tenure];
                        if (land_tenure)
                            layer.bindPopup(land_tenure.name);
                        else
                            layer.bindPopup(feature.properties.land_tenure);
                    }
                });

                map.addLayer(indigenous_lands_layer);
                layers_control.addOverlay(indigenous_lands_layer, 'Terras indígenas');

                map.on('overlayadd', function (eventLayer) {
                    // Switch to the Population legend...
                    if (eventLayer.name === 'Terras indígenas') {
                        legend_control.addTo(this);
                    }
                });
                map.on('overlayremove', function (eventLayer) {
                    if (eventLayer.name === 'Terras indígenas') {
                        this.removeControl(legend_control);
                    }
                });

                legend_control.addTo(map);
                //var sidebar = L.control.sidebar('sidebar').addTo(map);
            });
        }
    ]);
})(angular);