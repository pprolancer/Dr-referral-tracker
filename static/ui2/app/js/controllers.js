app.controller("MainCtrl", ['$scope', '$rootScope', '$http', '$window', function($scope, $rootScope, $http, $window) {
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

}]);

app.controller("DashboardCtrl", ['$scope', '$rootScope', '$http', function($scope, $rootScope, $http) {
    // $scope.$on('$viewContentLoaded', function() {
    // });
}]);

app.controller("OrganizationCtrl", ['$scope', '$rootScope', '$http', 'uiGridConstants', function($scope, $rootScope, $http, uiGridConstants) {
    $scope.sortingOptions = null;
    $scope.filteringOptions = [];
    $scope.paginationOptions = {
        page: 1,
    }
    $scope.organizationGridOpt = {
        paginationPageSizes: [10],
        paginationPageSize: 10,
        useExternalPagination: true,
        useExternalSorting: true,
        columnDefs: [
            {name: 'id', 'displayName': 'ID', width: 60},
            {name: 'org_name', 'displayName': 'Name'},
            {name: 'org_type', 'displayName': 'Type', width: 80},
            {name: 'org_contact_name', 'displayName': 'Contact Name'},
            {name: 'org_phone', 'displayName': 'Phone', width: 120},
            {name: 'org_email', 'displayName': 'Email', width: 200},
            {name: 'org_special', 'displayName': 'Special', width: 100,
                cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope fa" ng-class="{true:\'fa-check text-success\', false:\'fa-close text-danger\'}[row.entity.org_special==true]"></div>'
            }
        ],
        onRegisterApi: function(gridApi) {
            $scope.gridApi = gridApi;
            gridApi.core.on.sortChanged($scope, function(grid, sortColumns) {
                if (sortColumns.length == 0) {
                    $scope.sortingOptions = null;
                } else {
                    var col = sortColumns[0];
                    $scope.sortingOptions = (col.sort.direction==uiGridConstants.DESC?"-":"") + col.field;
                }
                $scope.getPage();
            });
            gridApi.pagination.on.paginationChanged($scope, function (newPage, pageSize) {
                $scope.paginationOptions.page = newPage;
                // $scope.paginationOptions.pageSize = pageSize;
                $scope.getPage();
            });
        }
    };
    $scope.getPage = function() {
        var url = "/api/v1/organization/?page="+$scope.paginationOptions.page;
        if ($scope.sortingOptions) {
            url += ("&ordering="+$scope.sortingOptions);
        }
        $http.get(url).
        then(function(response) {
            var pg = response.data.pagination;
            $scope.organizationGridOpt.data = response.data.results;
            $scope.organizationGridOpt.totalItems = pg.count;
            $scope.organizationGridOpt.paginationCurrentPage = pg.current_page;
            $scope.organizationGridOpt.paginationPageSize = pg.page_size;
        }, function(response) {
            app.utils.showDefaultServerError(response);
        });
    }
    $scope.getPage();
}]);

app.controller('PageContentController', ['$scope', function($scope) {

    $scope.$on('$includeContentLoaded', function() {
        Layout.fixContentHeight();
    });
}]);
