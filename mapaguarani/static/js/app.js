(function(angular) {
  'use strict';

  // Declare app level module which depends on views, and components
  var app = angular.module('mapaguarani', [
    //'ngRoute',
    //'leaflet-directive',
    'ui.router',
    'mapaguarani.filters',
    'mapaguarani.directives',
    'mapaguarani.controllers',
    'mapaguarani.services'
  ]);

  app.config([
  	'$stateProvider',
  	'$urlRouterProvider',
  	'$locationProvider',
  	'$httpProvider',
  	function($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider) {

  		$locationProvider.html5Mode({
  			enabled: false,
  			requireBase: false
  		});
  		$locationProvider.hashPrefix('!');

      $stateProvider
      .state('home', {
        url: '/',
        controller: 'HomeCtrl',
        templateUrl: '/static/views/home.html',
        resolve: {
          VillagesData: [
            'GuaraniService',
            function(Guarani) {
              return Guarani.villages.get().$promise;
            }
          ],
          LandsData: [
            'GuaraniService',
            function(Guarani) {
              return Guarani.lands.get().$promise;
            }
          ]
        }
      })
      .state('home.village', {
        url: 'villages/:id/',
        controller: 'SingleCtrl',
        templateUrl: '/static/views/partials/single.html',
        resolve: {
          Data: [
            'GuaraniService',
            '$stateParams',
            function(Guarani) {
              return Guarani.villages.get({id: $stateParams.id}).$promise;
            }
          ]
        }
      })
      .state('home.land', {
        url: 'lands/:id/',
        controller: 'SingleCtrl',
        templateUrl: '/static/views/single.html',
        resolve: {
          Data: [
            'GuaraniService',
            '$stateParams',
            function(Guarani) {
              return Guarani.lands.get({id: $stateParams.id}).$promise;
            }
          ]
        }
      });


      /*
      * Trailing slash rule
      */
      $urlRouterProvider.rule(function($injector, $location) {
      	var path = $location.path(),
      	search = $location.search(),
      	params;

      	// check to see if the path already ends in '/'
      	if (path[path.length - 1] === '/') {
      		return;
      	}

      	// If there was no search string / query params, return with a `/`
      	if (Object.keys(search).length === 0) {
      		return path + '/';
      	}

      	// Otherwise build the search string and return a `/?` prefix
      	params = [];
      	angular.forEach(search, function(v, k){
      		params.push(k + '=' + v);
      	});

      	return path + '/?' + params.join('&');
      });

    }
  ]);

})(angular);
