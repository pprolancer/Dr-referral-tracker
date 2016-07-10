app.controller('PageContentController', function($scope) {

    $scope.$on('$includeContentLoaded', function() {
        Layout.fixContentHeight();
    });
});

app.controller("MainCtrl", function($scope, $rootScope, $http, $window, Utils) {
    // load current user
    $rootScope.currentUser = {};
    $rootScope.pageLoaded = false;
    $rootScope.$global.TreatingProviderListCtrl = {}
    $rootScope.$global.OrganizationListCtrl = {}

    $rootScope.$global.TreatingProviderListCtrl.typeChoices = [
        {
            "value": "PA",
            "display_name": "Physician Assistant"
        }, {
            "value": "D",
            "display_name": "Doctor"
        }, {
            "value": "N",
            "display_name": "Nurse"
        }, {
            "value": "NP",
            "display_name": "Nurse Practitioner"
        }
    ];
    $rootScope.$global.OrganizationListCtrl.typeChoices = [
        {
            "display_name": "Marketing",
            "value": "MAR"
        }, {
            "display_name": "Insurance",
            "value": "INS"
        }, {
            "display_name": "Internal",
            "value": "INT"
        }, {
            "display_name": "Work comp.",
            "value": "WKC"
        }, {
            "display_name": "Healthcare Provider",
            "value": "HCP"
        }
    ];

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
        return Array.from(arguments).indexOf($rootScope.$state.current.name)>=0? 'active': '';
    }

});

app.controller("DashboardCtrl", function($scope, $rootScope) {
    // $scope.$on('$viewContentLoaded', function() {
    // });
});

/******************************************************************
********************* Organization controllers *****************
*******************************************************************/

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
                {name: 'org_type', 'displayName': 'Type',
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope">{{grid.appScope.getDisplayType(row.entity.org_type)}}</div>'
                },
                {name: 'org_contact_name', 'displayName': 'Contact Name'},
                {name: 'org_phone', 'displayName': 'Phone', width: 120},
                {name: 'org_email', 'displayName': 'Email', width: 200},
                {name: 'org_special', 'displayName': 'Special', width: 80,
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

    $scope.getDisplayType = function(type) {
        var choice = $global.typeChoices.filter(function(v) {
            return v.value==type
        })[0];
        return choice? choice.display_name: type;
    };

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
            if ($global && $global.gridOptions) {
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

/******************************************************************
********************* ReferringEntity controllers *****************
*******************************************************************/

app.controller("ReferringEntityListCtrl", function($scope, $rootScope, $state, $stateParams, ReferringEntityService, Utils, GeneralUiGrid, $uibModal) {
    $scope.loadingGrid = false;
    $scope.sortingOptions = null;
    $scope.filteringOptions = [];
    $scope.paginationOptions = {
        page: 1,
    };
    if (!$rootScope.$global.ReferringEntityListCtrl) {
        $rootScope.$global.ReferringEntityListCtrl = {}
    }

    var initialized = true,
        $global = $rootScope.$global.ReferringEntityListCtrl;
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
                {name: 'entity_name', 'displayName': 'Name',
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope"><a class="text text-primary" href="{{grid.appScope.$state.href(\'referring_entity-edit\', {id: row.entity.id})}}">{{row.entity.entity_name}}</a></div>'
                },
                {name: 'entity_title', 'displayName': 'Title'},
                {name: 'organization', 'displayName': 'Organization',
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope"><a class="text text-primary" href="{{grid.appScope.$state.href(\'organization-edit\', {id: row.entity.organization})}}">{{row.entity._organization.org_name}}</a></div>'
                    // cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope">{{row.entity.organization.org_name}}</div>'
                },
                {name: 'entity_phone', 'displayName': 'Phone', width: 120},
                {name: 'entity_email', 'displayName': 'Email', width: 200},
                {name: 'entity_special', 'displayName': 'Special', width: 100,
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope fa" ng-class="{true:\'fa-check text-success\', false:\'fa-close text-danger\'}[row.entity.entity_special==true]"></div>'
                },
                {name: 'action', 'displayName': 'Action', width: 80, enableColumnMenu: false, enableSorting: false,
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope"><a href="{{grid.appScope.$state.href(\'referring_entity-edit\', {id: row.entity.id})}}" class="text-primary" title="Edit"><span class="fa fa-pencil action-icon"></span></a> | <a ng-click="grid.appScope.showDeleteConfirm(row.entity.id)" class="text-danger" title="Delete"><span class="fa fa-trash action-icon"></span></a></div>'
                },
            ],
            // onRegisterApi: GeneralUiGrid.onRegisterApi($scope)
        };
    }
    $global.gridOptions.onRegisterApi = GeneralUiGrid.onRegisterApi($scope);
    $scope.getPage = GeneralUiGrid.getPage($scope, ReferringEntityService, $global.gridOptions);
    if (!initialized) {
        $scope.getPage();
    }

    $scope.showDeleteConfirm = function(id) {
        var getPage = $scope.getPage;
        var $global = $rootScope.$global.ReferringEntityListCtrl;
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
                    ReferringEntityService.delete({id: $scope.selectedId}, function(response) {
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

app.controller("ReferringEntityNewCtrl", function($scope, $rootScope, $state,$stateParams, ReferringEntityService, OrganizationService, Utils) {
    var $global = $rootScope.$global.ReferringEntityListCtrl;
    $scope.selectedRecord = new ReferringEntityService();
    OrganizationService.query({page_size: 0}, function(response) {
        $scope.organizations = response.results;
    });
    $scope.addRecord = function() {
        $scope.saving = true;
        $scope.selectedRecord.$save().then(function(response) {
            if ($global && $global.gridOptions) {
                $global.gridOptions.data.splice(0, 0, response);
            }
            $state.go('referring_entity-list');
            Utils.showDefaultServerSuccess(response);
        }, function(response) {
            Utils.showDefaultServerError(response);
        }).finally(function() {
            $scope.saving = false;
        });
    };
});

app.controller("ReferringEntityEditCtrl", function($scope, $rootScope, $state,$stateParams, ReferringEntityService, OrganizationService, Utils) {
    var $global = $rootScope.$global.ReferringEntityListCtrl;
    OrganizationService.query({page_size: 0}, function(response) {
        $scope.organizations = response.results;
    });
    $scope.updateRecord = function() {
        if (!$scope.selectedRecord) {
            return;
        }
        $scope.saving = true;
        $scope.selectedRecord.$update().then(function(response) {
            var data = ($global && $global.gridOptions)? $global.gridOptions.data: [];
            var idx = Utils.findByProperty(data, 'id', response.id);
            if (idx >= 0) {
                $global.gridOptions.data[idx] = response;
            }
            $state.go('referring_entity-list');
            Utils.showDefaultServerSuccess(response);
        }, function(response) {
            Utils.showDefaultServerError(response);
        }).finally(function() {
            $scope.saving = false;
        });
    };
    $scope.loadRecord=function() {
        ReferringEntityService.get({id: $stateParams.id}, function(record) {
            $scope.selectedRecord = record;
        }, function(response) {
            Utils.showDefaultServerError(response);
            $state.go('referring_entity-list');
        });
    };
    $scope.loadRecord();
});

/******************************************************************
********************* TreatingProvider controllers *****************
*******************************************************************/

app.controller("TreatingProviderListCtrl", function($scope, $rootScope, $state, $stateParams, TreatingProviderService, Utils, GeneralUiGrid, $uibModal) {
    $scope.loadingGrid = false;
    $scope.sortingOptions = null;
    $scope.filteringOptions = [];
    $scope.paginationOptions = {
        page: 1,
    };
    if (!$rootScope.$global.TreatingProviderListCtrl) {
        $rootScope.$global.TreatingProviderListCtrl = {}
    }

    var initialized = true,
        $global = $rootScope.$global.TreatingProviderListCtrl;
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
                {name: 'provider_name', 'displayName': 'Name',
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope"><a class="text text-primary" href="{{grid.appScope.$state.href(\'treating_provider-edit\', {id: row.entity.id})}}">{{row.entity.provider_name}}</a></div>'
                },
                {name: 'provider_title', 'displayName': 'Title'},
                {name: 'provider_type', 'displayName': 'Type',
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope">{{grid.appScope.getDisplayType(row.entity.provider_type)}}</div>'
                },
                {name: 'action', 'displayName': 'Action', width: 80, enableColumnMenu: false, enableSorting: false,
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope"><a href="{{grid.appScope.$state.href(\'treating_provider-edit\', {id: row.entity.id})}}" class="text-primary" title="Edit"><span class="fa fa-pencil action-icon"></span></a> | <a ng-click="grid.appScope.showDeleteConfirm(row.entity.id)" class="text-danger" title="Delete"><span class="fa fa-trash action-icon"></span></a></div>'
                },
            ],
            // onRegisterApi: GeneralUiGrid.onRegisterApi($scope)
        };
    }
    $global.gridOptions.onRegisterApi = GeneralUiGrid.onRegisterApi($scope);
    $scope.getPage = GeneralUiGrid.getPage($scope, TreatingProviderService, $global.gridOptions);
    if (!initialized) {
        $scope.getPage();
    }

    $scope.getDisplayType = function(type) {
        var choice = $global.typeChoices.filter(function(v) {
            return v.value==type
        })[0];
        return choice? choice.display_name: type;
    };

    $scope.showDeleteConfirm = function(id) {
        var getPage = $scope.getPage;
        var $global = $rootScope.$global.TreatingProviderListCtrl;
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
                    TreatingProviderService.delete({id: $scope.selectedId}, function(response) {
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

app.controller("TreatingProviderNewCtrl", function($scope, $rootScope, $state,$stateParams, TreatingProviderService, Utils) {
    var $global = $rootScope.$global.TreatingProviderListCtrl;
    $scope.selectedRecord = new TreatingProviderService();
    $scope.addRecord = function() {
        $scope.saving = true;
        $scope.selectedRecord.$save().then(function(response) {
            if ($global && $global.gridOptions) {
                $global.gridOptions.data.splice(0, 0, response);
            }
            $state.go('treating_provider-list');
            Utils.showDefaultServerSuccess(response);
        }, function(response) {
            Utils.showDefaultServerError(response);
        }).finally(function() {
            $scope.saving = false;
        });
    };
});

app.controller("TreatingProviderEditCtrl", function($scope, $rootScope, $state,$stateParams, TreatingProviderService, Utils) {
    var $global = $rootScope.$global.TreatingProviderListCtrl;
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
            $state.go('treating_provider-list');
            Utils.showDefaultServerSuccess(response);
        }, function(response) {
            Utils.showDefaultServerError(response);
        }).finally(function() {
            $scope.saving = false;
        });
    };
    $scope.loadRecord=function() {
        TreatingProviderService.get({id: $stateParams.id}, function(record) {
            $scope.selectedRecord = record;
        }, function(response) {
            Utils.showDefaultServerError(response);
            $state.go('treating_provider-list');
        });
    };
    $scope.loadRecord();
});

/******************************************************************
********************* PatientVisit controllers *****************
*******************************************************************/

app.controller("PatientVisitListCtrl", function($scope, $rootScope, $state, $stateParams, PatientVisitService, Utils, GeneralUiGrid, $uibModal) {
    $scope.loadingGrid = false;
    $scope.sortingOptions = null;
    $scope.filteringOptions = [];
    $scope.paginationOptions = {
        page: 1,
    };
    if (!$rootScope.$global.PatientVisitListCtrl) {
        $rootScope.$global.PatientVisitListCtrl = {}
    }

    var initialized = true,
        $global = $rootScope.$global.PatientVisitListCtrl;
    if (!$global.gridOptions) {
        initialized = false;
        $global.gridOptions = {
            paginationPageSizes: [10],
            paginationPageSize: 10,
            useExternalPagination: true,
            useExternalSorting: true,
            rowHeight: 35,
            columnDefs: [
                {name: 'id', 'displayName': 'ID', width: 60,
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope"><a class="text text-primary" href="{{grid.appScope.$state.href(\'patient_visit-edit\', {id: row.entity.id})}}">{{row.entity.id}}</a></div>'
                },
                {name: 'referring_entity', 'displayName': 'Referring Entity',
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope"><a class="text text-primary" href="{{grid.appScope.$state.href(\'referring_entity-edit\', {id: row.entity.referring_entity})}}">{{row.entity._referring_entity.entity_name}}</a></div>'
                },
                {name: 'treating_provider', 'displayName': 'Treating Provider',
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope"><a class="text text-primary" href="{{grid.appScope.$state.href(\'treating_provider-edit\', {id: row.entity.treating_provider})}}">{{row.entity._treating_provider.provider_name}}</a></div>'
                },
                {name: 'visit_date', 'displayName': 'Visit Date',
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope">{{row.entity.visit_date|date: \'MMM dd, yyyy\'}}</div>'
                },
                {name: 'visit_appointment_time', 'displayName': 'Appointment Time',
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope">{{row.entity.visit_appointment_time|date: \'hh:mm a\'}}</div>'
                },
                {name: 'visit_actual_time', 'displayName': 'Actual Time',
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope">{{row.entity.visit_actual_time|date: \'hh:mm a\'}}</div>'
                },
                {name: 'action', 'displayName': 'Action', width: 80, enableColumnMenu: false, enableSorting: false,
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope"><a href="{{grid.appScope.$state.href(\'patient_visit-edit\', {id: row.entity.id})}}" class="text-primary" title="Edit"><span class="fa fa-pencil action-icon"></span></a> | <a ng-click="grid.appScope.showDeleteConfirm(row.entity.id)" class="text-danger" title="Delete"><span class="fa fa-trash action-icon"></span></a></div>'
                },
            ],
            // onRegisterApi: GeneralUiGrid.onRegisterApi($scope)
        };
    }
    $global.gridOptions.onRegisterApi = GeneralUiGrid.onRegisterApi($scope);
    $scope.getPage = GeneralUiGrid.getPage($scope, PatientVisitService, $global.gridOptions);
    if (!initialized) {
        $scope.getPage();
    }

    $scope.showDeleteConfirm = function(id) {
        var getPage = $scope.getPage;
        var $global = $rootScope.$global.PatientVisitListCtrl;
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
                    PatientVisitService.delete({id: $scope.selectedId}, function(response) {
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

app.controller("PatientVisitNewCtrl", function($scope, $rootScope, $state,$stateParams, PatientVisitService, ReferringEntityService, TreatingProviderService, Utils) {
    var $global = $rootScope.$global.PatientVisitListCtrl;
    $scope.selectedRecord = new PatientVisitService();
    ReferringEntityService.query({page_size: 0}, function(response) {
        $scope.referring_entities = response.results;
    });
    TreatingProviderService.query({page_size: 0}, function(response) {
        $scope.treating_providers = response.results;
    });
    $scope.addRecord = function() {
        $scope.saving = true;
        $scope.selectedRecord.$save().then(function(response) {
            if ($global && $global.gridOptions) {
                $global.gridOptions.data.splice(0, 0, response);
            }
            $state.go('patient_visit-list');
            Utils.showDefaultServerSuccess(response);
        }, function(response) {
            Utils.showDefaultServerError(response);
        }).finally(function() {
            $scope.saving = false;
        });
    };
});

app.controller("PatientVisitEditCtrl", function($scope, $rootScope, $state,$stateParams, PatientVisitService, ReferringEntityService, TreatingProviderService, Utils) {
    var $global = $rootScope.$global.PatientVisitListCtrl;
    ReferringEntityService.query({page_size: 0}, function(response) {
        $scope.referring_entities = response.results;
    });
    TreatingProviderService.query({page_size: 0}, function(response) {
        $scope.treating_providers = response.results;
    });
    $scope.updateRecord = function() {
        if (!$scope.selectedRecord) {
            return;
        }
        $scope.saving = true;

        $scope.selectedRecord.$update().then(function(response) {
            var data = ($global && $global.gridOptions)? $global.gridOptions.data: [];
            var idx = Utils.findByProperty(data, 'id', response.id);
            if (idx >= 0) {
                $global.gridOptions.data[idx] = response;
            }
            $state.go('patient_visit-list');
            Utils.showDefaultServerSuccess(response);
        }, function(response) {
            Utils.showDefaultServerError(response);
        }).finally(function() {
            $scope.saving = false;
        });
    };
    $scope.loadRecord=function() {
        PatientVisitService.get({id: $stateParams.id}, function(record) {
            $scope.selectedRecord = record;
        }, function(response) {
            Utils.showDefaultServerError(response);
            $state.go('patient_visit-list');
        });
    };
    $scope.loadRecord();
});
