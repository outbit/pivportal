var pivportalApp = angular.module('pivportalApp', [ 'ngRoute', 'pivportalControllers', 'satellizer', 'toaster']);

pivportalApp.config(['$routeProvider', '$httpProvider', '$authProvider',
  function($routeProvider, $httpProvider, $authProvider) {
      // Routes
      $routeProvider.
        when('/login', {
         templateUrl: 'templates/login.html',
         controller: 'pivportalLoginCtrl',
        }).
        otherwise( {
         templateUrl: 'templates/dash.html',
         controller: 'pivportalAuthCtrl',
        });
  }]);