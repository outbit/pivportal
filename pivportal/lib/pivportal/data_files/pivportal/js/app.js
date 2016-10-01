var pivportalApp = angular.module('pivportalApp', [ 'ngRoute', 'pivportalControllers', 'satellizer', 'toaster']);

pivportalApp.config(['$routeProvider', '$httpProvider', '$authProvider',
  function($routeProvider, $httpProvider, $authProvider) {
      // Login URL
      $authProvider.loginUrl = '/api/rest/user/login'

      // Routes
      $routeProvider.
        when('/login', {
         templateUrl: 'templates/login.html',
         controller: 'pivportalLoginCtrl',
         resolve: {
            skipIfLoggedIn: skipIfLoggedIn
         }
        }).
        when('/dash', {
         templateUrl: 'templates/dash.html',
         controller: 'pivportalAuthCtrl',
         resolve: {
            loginRequired: loginRequired
         }
        }).
        otherwise( {
         templateUrl: 'templates/dash.html',
         controller: 'pivportalAuthCtrl',
         resolve: {
            loginRequired: loginRequired
         }
        });

    // Login Required, redirect to login page
    function loginRequired($q, $auth, $location) {
        var deferred = $q.defer();
        if ($auth.isAuthenticated()) {
            deferred.resolve();
        } else {
            $location.path('/login');
        }
        return deferred.promise;
    }

    // Users Already Logged In, Skip Login
    function skipIfLoggedIn($q, $auth) {
      var deferred = $q.defer();
      if ($auth.isAuthenticated()) {
        deferred.reject();
      } else {
        deferred.resolve();
      }
      return deferred.promise;
    }
  }]);