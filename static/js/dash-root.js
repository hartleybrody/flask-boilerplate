BaseApp.controller('DashRootController', function($scope, $timeout, $interval, $location, $controller) {

    var app = this;
    angular.extend(app, $controller('BaseController', {$scope: $scope}));

    app.init = function(){
        app.base_init()

    }

    app.init();  // always call this last
})
