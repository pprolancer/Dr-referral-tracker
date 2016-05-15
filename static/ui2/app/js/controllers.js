app.controller("MainCtrl", function($scope, $rootScope, $http, $window) {
    // load current user
    $rootScope.currentUser = {};
    $rootScope.pageLoaded = false;
    $scope.$on('$viewContentLoaded', function() {
        if ($rootScope.pageLoaded) {
            Index.initCharts();
        }
    });
    $http.get("/api/v1/session/").
    then(function(response) {
        $rootScope.currentUser = response.data;
        $rootScope.pageLoaded = true;
        $('body').css('background-image', 'none').removeClass('hide');
        Index.initCharts();
    }, function(response) {
        if (response.status == 403) {
            $window.location.href = '/';
        } else {
            app.utils.showDefaultServerError(response)
        }
    });

    // logout function
    $scope.logout = function() {
        $http.delete('/api/v1/session').
        then(function(response) {
            $window.location.href = '/';
        }, function(response) {
            app.utils.showDefaultServerError(response)
        });
    }

    $scope.menuActiveIf = function(pageName) {
        return $rootScope.$state.current.name == pageName? 'active': '';
    }

});

app.controller("DashboardCtrl", function($scope, $rootScope, $http) {
    // $scope.$on('$viewContentLoaded', function() {
    // });
});

app.controller("OrganizationCtrl", function($scope, $rootScope, $http) {
    // $scope.$on('$viewContentLoaded', function() {
    // });
});

app.controller('PageContentController', ['$scope', function($scope) {

    $scope.$on('$includeContentLoaded', function() {
        Layout.fixContentHeight();
    });
}]);
