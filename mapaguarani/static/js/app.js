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
    'mapaguarani.services',
    'djangular'
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
        url: '/?content&filter&page&{z:int}&{x:int}&{y:int}',
        reloadOnSearch: false,
        controller: 'HomeCtrl',
        templateUrl: '/static/views/home.html',
        params: {
          'clustered': undefined
        },
      })
      .state('village', {
        url: '/villages/:id/',
        controller: 'SingleCtrl',
        templateUrl: '/static/views/single-village.html',
        data: {
          contentType: 'sites',
        },
        params: {
          focus: true
        },
        resolve: {
          Data: [
            'GuaraniService',
            '$stateParams',
            function(Guarani, $stateParams) {
              return Guarani.villages.get({id: $stateParams.id}).$promise;
            }
          ]
        }
      })
      .state('land', {
        url: '/lands/:id/',
        controller: 'SingleCtrl',
        templateUrl: '/static/views/single-land.html',
        data: {
          contentType: 'sites',
        },
        params: {
          focus: true
        },
        resolve: {
          Data: [
            'GuaraniService',
            '$stateParams',
            function(Guarani, $stateParams) {
              return Guarani.lands.get({id: $stateParams.id}).$promise;
            }
          ]
        }
      })
      .state('site', {
        url: '/sites/:id/',
        controller: 'SingleCtrl',
        templateUrl: '/static/views/single-archaeological.html',
        data: {
          contentType: 'sites',
        },
        params: {
          focus: true
        },
        resolve: {
          Data: [
            'GuaraniService',
            '$stateParams',
            function(Guarani, $stateParams) {
              return Guarani.sites.get({id: $stateParams.id}).$promise;
            }
          ]
        }
      })
      .state('projetc', {
        url: '/project/:id/',
        controller: 'SingleProjectCtrl',
        templateUrl: '/static/views/single-project.html',
        data: {
          contentType: 'project',
        },
        params: {
          focus: true
        },
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
