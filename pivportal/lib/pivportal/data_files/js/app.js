var outbitApp = angular.module('outbitApp', [ 'ngRoute', 'outbitControllers', 'satellizer', 'toaster']);

outbitApp.run(function($rootScope){
      // Global Vars
      $rootScope.outbitapi_ip = window.location.hostname
      $rootScope.outbitapi_port = "8088"
});

outbitApp.config(['$routeProvider', '$httpProvider', '$authProvider',
  function($routeProvider, $httpProvider, $authProvider) {
      // Login URL
      $authProvider.loginUrl = '//' + window.location.hostname + ':8088/login'
      // The below doesnt work for some reason??
      //$authProvider.loginUrl = '//' + $rootScope.outbitapi_ip + ':' + $rootScope.outbitapi_port + '/login';

      // Support Cross-Domain
      $httpProvider.defaults.useXDomain = true;
      delete $httpProvider.defaults.headers.common["X-Requested-With"];

      // Routes
      $routeProvider.
        when('/login', {
         templateUrl: 'templates/login.html',
         controller: 'outbitLoginCtrl',
         resolve: {
            skipIfLoggedIn: skipIfLoggedIn
         }
        }).
        when('/logout', {
         template: null,
         controller: 'outbitLogoutCtrl'
        }).
        when('/jobs', {
         templateUrl: 'templates/jobs.html',
         controller: 'outbitJobsCtrl',
         resolve: {
            loginRequired: loginRequired
         }
        }).
        when('/actions', {
         templateUrl: 'templates/actions.html',
         controller: 'outbitActionsCtrl',
         resolve: {
            loginRequired: loginRequired
         }
        }).
        when('/user', {
         templateUrl: 'templates/user.html',
         controller: 'outbitUserCtrl',
         resolve: {
            loginRequired: loginRequired
         }
        }).
        otherwise( {
         templateUrl: 'templates/jobs.html',
         controller: 'outbitJobsCtrl',
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