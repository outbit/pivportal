var pivportalControllers = angular.module('pivportalControllers', []);

pivportalControllers.controller('pivportalAuthCtrl', ['$auth', '$scope', '$http', '$rootScope', "toaster",
  function ($auth, $scope, $http, $rootScope, toaster) {
      $scope.authorize_request = function(username, requestid, client_ip, authorized) {
            // Somehow post data
              $http.post('/api/request/auth', {"username": username, "requestid": requestid, "client_ip": client_ip, "authorized": authorized}).success(function (data) {
          }).error(function (data) {
              console.log(data);
          });
      };

      $http.post('/api/request/list', {"username": "whitesid"}).success(function (data) {
          $scope.auth_requests = data;
      }).error(function (data) {
          console.log(data);
      });
  }
]);
