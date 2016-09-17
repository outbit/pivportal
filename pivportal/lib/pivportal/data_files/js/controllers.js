var pivportalControllers = angular.module('pivportalControllers', []);

pivportalControllers.controller('pivportalAuthCtrl', ['$auth', '$scope', '$http', '$rootScope', "toaster", "$interval",
  function ($auth, $scope, $http, $rootScope, toaster, $interval) {
      $scope.authorize_request = function(username, requestid, client_ip, authorized) {
            // Somehow post data
              $http.post('/api/rest/request/auth', {"username": username, "requestid": requestid, "client_ip": client_ip, "authorized": authorized}).success(function (data) {
              $scope.list_requests(); // Update list
          }).error(function (data) {
              console.log(data);
          });
      };


      $scope.list_requests = function(){
          $http.post('/api/rest/request/list', {"username": "whitesid"}).success(function (data) {
              $scope.auth_requests = data;
          }).error(function (data) {
              console.log(data);
          });
      }

      // Go ahead and get list of requests
      $scope.list_requests();

      // update requests list every 5 seconds
      $interval($scope.list_requests, 5000);
  }
]);
