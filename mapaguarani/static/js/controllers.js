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
            });

            // Google maps - leaflet 0.7
            //var gm_roadmap = new L.Google('ROADMAP');
            //var gm_terrain = new L.Google('TERRAIN');
            //var gm_hybrid = new L.Google('HYBRID');
            //var baselayers = {
            //    'Mapa': gm_roadmap,
            //    'Hibrido': gm_hybrid,
            //    'Terreno': gm_terrain
            //};
            //map.addLayer(gm_hybrid);

            // Mapbox - leaflet 1.0 compatible
            var access_token = 'pk.eyJ1IjoiYnJ1bm9zbWFydGluIiwiYSI6IjM1MTAyYTJjMWQ3NmVmYTg0YzQ0ZWFjZTg0MDZiYzQ3In0.ThelegmeGkO5Vwd6KTu6xA'
            var mapbox_url = 'http://api.tiles.mapbox.com/v4/{mapid}/{z}/{x}/{y}.png?access_token={access_token}'
            var mapbox_satalite = L.tileLayer(mapbox_url, {mapid: 'mapbox.satellite', access_token: access_token}),
                mapbox_streets   = L.tileLayer(mapbox_url, {mapid: 'mapbox.streets', access_token: access_token});

            var baselayers = {
                'Mapa': mapbox_streets,
                'Satelite': mapbox_satalite
            };
            map.addLayer(mapbox_satalite);
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
                    disableClusteringAtZoom :7
                });
                markers.addLayer(villages_layer);
                map.addLayer(markers);
                layers_control.addOverlay(markers, 'Aldeias Indígenas');
            });

            IndigenousLands.get({}, function(lands){
                var indigenous_lands_layer = L.geoJson(lands, {
                    //style: function (feature) {
                    //    return {color: feature.properties.color};
                    //},
                    //onEachFeature: function (feature, layer) {
                    //    layer.bindPopup(feature.properties.description);
                    //}
                });

                map.addLayer(indigenous_lands_layer);
                layers_control.addOverlay(indigenous_lands_layer, 'Terras indígenas');
            });
        }
    ]);
})(angular);