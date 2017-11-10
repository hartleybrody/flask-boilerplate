angular.module('DashRootApp', [])
    .controller('DashRootController', function($scope, $timeout, $interval, $location) {

        var app = this;

        app.init = function(){

            $scope.users = window.js_init.users;
            console.log($scope.users)

        }

        // always call this last, after every other function has been defined
        app.init();
    })
    .filter('safe', function($sce) {
        return function(val) {
            return $sce.trustAsHtml(val);
        };
    })
