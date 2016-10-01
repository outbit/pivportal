var pivportalControllers = angular.module('pivportalControllers', []);

pivportalControllers.controller('pivportalLoginCtrl', ['$auth', '$scope', '$http', 'toaster',
  function ($auth, $scope, $http, toaster) {
    $scope.login = function() {
      $auth.login().then(function(data) {
        console.log(data)
      })
      .catch(function(response){ // If login is unsuccessful, display relevant error message.
               console.log(response.data)
               toaster.pop({
                type: 'error',
                title: 'Login Failed',
                body: response.data,
                showCloseButton: true,
                timeout: 0
                });
       });
    }

  // Go Ahead and Login on Page Load (Using Client Cert)
  $scope.login();
  }
])

pivportalControllers.controller('pivportalAuthCtrl', ['$auth', '$scope', '$http', '$rootScope', "toaster", "$interval",
  function ($auth, $scope, $http, $rootScope, toaster, $interval) {
      $scope.authorize_request = function(username, requestid, client_ip, authorized) {
            // Somehow post data
              $http.post('/api/rest/request/auth', {"requestid": requestid, "client_ip": client_ip, "authorized": authorized}).success(function (data) {
              $scope.list_requests(); // Update list
          }).error(function (data) {
              toaster.pop({
                type: 'error',
                body: data,
                showCloseButton: true,
                });
              console.log(data);
          });
      };


      $scope.list_requests = function(){
              $http.post('/api/rest/request/list').success(function (data) {
              $scope.auth_requests = data;
          }).error(function (data) {
              toaster.pop({
                type: 'error',
                body: data,
                showCloseButton: true,
                });
              console.log(data);
          });
      }

      // Go ahead and get list of requests
      $scope.list_requests();

      // update requests list every 5 seconds
      $interval($scope.list_requests, 5000);
  }
]);
