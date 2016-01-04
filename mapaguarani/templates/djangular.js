(function(angular) {
  'use strict';

    var djangular = angular.module('djangular', [])

    djangular.service('user', function () {
       return {
                  'username': '{{ user.username|escapejs }}',
                  'is_autenticated': 'True' === '{{ user.is_authenticated|escapejs }}'
              }
    });

})(angular);
