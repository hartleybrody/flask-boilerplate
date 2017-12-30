var BaseApp = angular.module('BaseApp', []);

BaseApp.controller('BaseController', function($scope, $timeout, $interval, $location) {

    var app = this;

    app.base_init = function(){
        _.each(window.js_init, function(v, k){
            $scope[k] = v
        })
    }

})
.filter('safe', function($sce) {
    return function(val) {
        return $sce.trustAsHtml(val);
    };
})