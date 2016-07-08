app.controller('PageContentController', function($scope) {

    $scope.$on('$includeContentLoaded', function() {
        Layout.fixContentHeight();
    });
});

app.controller("MainCtrl", function($scope, $rootScope, $http, $window, Utils) {
    // load current user
    $rootScope.currentUser = {};
    $rootScope.pageLoaded = false;
    $scope.$on('$viewContentLoaded', function() {
        if ($rootScope.pageLoaded) {
            Index.initCharts();
        }
    });
    $http.get(Utils.noCacheUrl("/api/v1/session/")).
    then(function(response) {
        $rootScope.currentUser = response.data;
        $rootScope.pageLoaded = true;
        $('body').css('background-image', 'none').removeClass('hide');
        Index.initCharts();
    }, function(response) {
        Utils.showDefaultServerError(response);
    });

    // logout function
    $scope.logout = function() {
        $http.delete('/api/v1/session').
        then(function(response) {
            window.location = '/?next=' + window.location.pathname;
        }, function(response) {
            Utils.showDefaultServerError(response)
        });
    }

    $scope.menuActiveIf = function(pageName) {
        return $rootScope.$state.current.name == pageName? 'active': '';
    }

});

app.controller("DashboardCtrl", function($scope, $rootScope) {
    // $scope.$on('$viewContentLoaded', function() {
    // });
});

app.controller("OrganizationListCtrl", function($scope, $rootScope, $state, $stateParams, OrganizationService, Utils, GeneralUiGrid, $uibModal) {
    $scope.loadingGrid = false;
    $scope.sortingOptions = null;
    $scope.filteringOptions = [];
    $scope.paginationOptions = {
        page: 1,
    };
    if (!$rootScope.$global.OrganizationListCtrl) {
        $rootScope.$global.OrganizationListCtrl = {}
    }

    var initialized = true,
        $global = $rootScope.$global.OrganizationListCtrl;
    if (!$global.gridOptions) {
        initialized = false;
        $global.gridOptions = {
            paginationPageSizes: [10],
            paginationPageSize: 10,
            useExternalPagination: true,
            useExternalSorting: true,
            rowHeight: 35,
            columnDefs: [
                {name: 'id', 'displayName': 'ID', width: 60},
                {name: 'org_name', 'displayName': 'Name',
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope"><a class="text text-primary" href="{{grid.appScope.$state.href(\'organization-edit\', {id: row.entity.id})}}">{{row.entity.org_name}}</a></div>'
                },
                {name: 'org_type', 'displayName': 'Type', width: 80},
                {name: 'org_contact_name', 'displayName': 'Contact Name'},
                {name: 'org_phone', 'displayName': 'Phone', width: 120},
                {name: 'org_email', 'displayName': 'Email', width: 200},
                {name: 'org_special', 'displayName': 'Special', width: 100,
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope fa" ng-class="{true:\'fa-check text-success\', false:\'fa-close text-danger\'}[row.entity.org_special==true]"></div>'
                },
                {name: 'action', 'displayName': 'Action', width: 80, enableColumnMenu: false, enableSorting: false,
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope"><a href="{{grid.appScope.$state.href(\'organization-edit\', {id: row.entity.id})}}" class="text-primary" title="Edit"><span class="fa fa-pencil action-icon"></span></a> | <a ng-click="grid.appScope.showDeleteConfirm(row.entity.id)" class="text-danger" title="Delete"><span class="fa fa-trash action-icon"></span></a></div>'
                },
            ],
            // onRegisterApi: GeneralUiGrid.onRegisterApi($scope)
        };
    }
    $global.gridOptions.onRegisterApi = GeneralUiGrid.onRegisterApi($scope);
    $scope.getPage = GeneralUiGrid.getPage($scope, OrganizationService, $global.gridOptions);
    if (!initialized) {
        $scope.getPage();
    }

    $scope.showDeleteConfirm = function(id) {
        var getPage = $scope.getPage;
        var $global = $rootScope.$global.OrganizationListCtrl;
        var data = $global.gridOptions? $global.gridOptions.data: [];
        var idx = Utils.findByProperty(data, 'id', id),
            gridOptions = $global.gridOptions;

        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'app/partials/confirm-modal.html',
            controller: function($scope, $uibModalInstance, Utils) {
                $scope.selectedId = id;
                $scope.deleting = false;
                $scope.removeRecord = function () {
                    $scope.deleting = true;
                    OrganizationService.delete({id: $scope.selectedId}, function(response) {
                        if (idx >= 0) {
                            gridOptions.data.splice(idx, 1);
                        }
                        Utils.showDefaultServerSuccess(response);
                        $uibModalInstance.close();
                    }, function(response) {
                        Utils.showDefaultServerError(response);
                    }).$promise.finally(function() {
                        $scope.deleting = false;
                    })

                };
                $scope.cancelRemove = function () {
                    $uibModalInstance.dismiss('cancel');
                };
            }
        });
    };
});

app.controller("OrganizationNewCtrl", function($scope, $rootScope, $state,$stateParams, OrganizationService, Utils) {
    var $global = $rootScope.$global.OrganizationListCtrl;
    $scope.selectedRecord = new OrganizationService();
    $scope.addRecord = function() {
        $scope.saving = true;
        $scope.selectedRecord.$save().then(function(response) {
            if ($global.gridOptions) {
                $global.gridOptions.data.splice(0, 0, response);
            }
            $state.go('organization-list');
            Utils.showDefaultServerSuccess(response);
        }, function(response) {
            Utils.showDefaultServerError(response);
        }).finally(function() {
            $scope.saving = false;
        });
    };
});

app.controller("OrganizationEditCtrl", function($scope, $rootScope, $state,$stateParams, OrganizationService, Utils) {
    var $global = $rootScope.$global.OrganizationListCtrl;
    $scope.updateRecord = function() {
        if (!$scope.selectedRecord) {
            return;
        }
        $scope.saving = true;
        $scope.selectedRecord.$update().then(function(response) {
            var data = $global.gridOptions? $global.gridOptions.data: [];
            var idx = Utils.findByProperty(data, 'id', response.id);
            if (idx >= 0) {
                $global.gridOptions.data[idx] = response;
            }
            $state.go('organization-list');
            Utils.showDefaultServerSuccess(response);
        }, function(response) {
            Utils.showDefaultServerError(response);
        }).finally(function() {
            $scope.saving = false;
        });
    };
    $scope.loadRecord=function() {
        OrganizationService.get({id: $stateParams.id}, function(record) {
            $scope.selectedRecord = record;
        }, function(response) {
            Utils.showDefaultServerError(response);
            $state.go('organization-list');
        });
    };
    $scope.loadRecord();
});
