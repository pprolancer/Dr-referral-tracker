app.controller('PageContentController', function($scope) {

    $scope.$on('$includeContentLoaded', function() {
        Layout.fixContentHeight();
    });
});

app.controller("MainCtrl", function($scope, $rootScope, $http, $window, Utils, ReferringEntityService, TreatingProviderService, OrganizationService) {
    // load current user
    $rootScope.currentUser = {};
    $rootScope.pageLoaded = false;
    $rootScope.$global.TreatingProvider = {}
    $rootScope.$global.Organization = {}
    $rootScope.$global.ReferringEntity = {}
    $rootScope.$global.PatientVisit = {}
    $rootScope.$global.PatientVisitsReport = {}

    $rootScope.$global.TreatingProvider.typeChoices = [
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
    $rootScope.$global.Organization.typeChoices = [
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
    };

    $scope.menuActiveIf = function(pageName) {
        return Array.from(arguments).indexOf($rootScope.$state.current.name)>=0? 'active': '';
    };

    $rootScope.loadReferringEntityCombo = function() {
        if (!$rootScope.$global.ReferringEntity.comboData) {
            ReferringEntityService.query({page_size: 0, ordering: 'entity_name', fields: 'id,entity_name'}, function(response) {
                $rootScope.$global.ReferringEntity.comboData = response.results;
            });
        }
    };

    $rootScope.loadTreatingProviderCombo = function() {
        if (!$rootScope.$global.TreatingProvider.comboData) {
            TreatingProviderService.query({page_size: 0, ordering: 'provider_name', fields: 'id,provider_name'}, function(response) {
                $rootScope.$global.TreatingProvider.comboData = response.results;
            });
        }
    };

    $rootScope.loadOrganizationCombo = function() {
        if (!$rootScope.$global.Organization.comboData) {
            OrganizationService.query({page_size: 0, ordering: 'org_name', fields: 'id,org_name'}, function(response) {
                $rootScope.$global.Organization.comboData = response.results;
            });
        }
    };


});

app.controller("DashboardCtrl", function($scope, $rootScope) {
    // $scope.$on('$viewContentLoaded', function() {
    // });
});

/******************************************************************
********************* Organization controllers *****************
*******************************************************************/

app.controller("OrganizationListCtrl", function($scope, $rootScope, $state, $stateParams, OrganizationService, Utils, GeneralUiGrid) {
    $scope.loadingGrid = false;
    $scope.sortingOptions = null;
    $scope.filteringOptions = [];
    $scope.paginationOptions = {
        page: 1,
    };
    if (!$rootScope.$global.Organization) {
        $rootScope.$global.Organization = {}
    }

    var initialized = true,
        $global = $rootScope.$global.Organization;
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
                }
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
});

app.controller("OrganizationNewCtrl", function($scope, $rootScope, $state,$stateParams, OrganizationService, Utils) {
    var $global = $rootScope.$global.Organization;
    $scope.selectedRecord = new OrganizationService();
    $scope.addRecord = function() {
        $scope.saving = true;
        $scope.selectedRecord.$save().then(function(response) {
            if ($global && $global.gridOptions) {
                $global.gridOptions.data.splice(0, 0, response);
            }
            $rootScope.$global.Organization.comboData = undefined;
            $state.go('organization-list');
            Utils.showDefaultServerSuccess(response);
        }, function(response) {
            Utils.showDefaultServerError(response);
        }).finally(function() {
            $scope.saving = false;
        });
    };
});

app.controller("OrganizationEditCtrl", function($scope, $rootScope, $state,$stateParams, OrganizationService, Utils, $uibModal) {
    var $global = $rootScope.$global.Organization;

    $scope.showDeleteConfirm = function() {
        if (!$scope.selectedRecord) {
            return;
        }
        var id = $scope.selectedRecord.id;
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
                        $rootScope.$global.Organization.comboData = undefined;
                        Utils.showDefaultServerSuccess(response);
                        $uibModalInstance.close();
                        $state.go('organization-list');
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
            $rootScope.$global.Organization.comboData = undefined;
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

app.controller("ReferringEntityListCtrl", function($scope, $rootScope, $state, $stateParams, ReferringEntityService, Utils, GeneralUiGrid) {
    $scope.loadingGrid = false;
    $scope.sortingOptions = null;
    $scope.filteringOptions = [];
    $scope.paginationOptions = {
        page: 1,
    };
    if (!$rootScope.$global.ReferringEntity) {
        $rootScope.$global.ReferringEntity = {}
    }

    var initialized = true,
        $global = $rootScope.$global.ReferringEntity;
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
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope">{{row.entity._organization.org_name}}</div>'
                },
                {name: 'entity_phone', 'displayName': 'Phone', width: 120},
                {name: 'entity_email', 'displayName': 'Email', width: 200},
                {name: 'entity_special', 'displayName': 'Special', width: 100,
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope fa" ng-class="{true:\'fa-check text-success\', false:\'fa-close text-danger\'}[row.entity.entity_special==true]"></div>'
                }
            ],
            // onRegisterApi: GeneralUiGrid.onRegisterApi($scope)
        };
    }
    $global.gridOptions.onRegisterApi = GeneralUiGrid.onRegisterApi($scope);
    $scope.getPage = GeneralUiGrid.getPage($scope, ReferringEntityService, $global.gridOptions);
    if (!initialized) {
        $scope.getPage();
    }

});

app.controller("ReferringEntityNewCtrl", function($scope, $rootScope, $state,$stateParams, ReferringEntityService, OrganizationService, Utils) {
    var $global = $rootScope.$global.ReferringEntity;
    $scope.selectedRecord = new ReferringEntityService();
    $rootScope.loadOrganizationCombo();
    $scope.addRecord = function() {
        $scope.saving = true;
        $scope.selectedRecord.$save().then(function(response) {
            if ($global && $global.gridOptions) {
                $global.gridOptions.data.splice(0, 0, response);
            }
            $rootScope.$global.ReferringEntity.comboData = undefined;
            $state.go('referring_entity-list');
            Utils.showDefaultServerSuccess(response);
        }, function(response) {
            Utils.showDefaultServerError(response);
        }).finally(function() {
            $scope.saving = false;
        });
    };
});

app.controller("ReferringEntityEditCtrl", function($scope, $rootScope, $state,$stateParams, ReferringEntityService, OrganizationService, Utils, $uibModal) {
    var $global = $rootScope.$global.ReferringEntity;
    $rootScope.loadOrganizationCombo();

    $scope.showDeleteConfirm = function() {
        if (!$scope.selectedRecord) {
            return;
        }
        var id = $scope.selectedRecord.id;
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
                        $rootScope.$global.ReferringEntity.comboData = undefined;
                        Utils.showDefaultServerSuccess(response);
                        $uibModalInstance.close();
                        $state.go('referring_entity-list');
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
            $rootScope.$global.ReferringEntity.comboData = undefined;
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

app.controller("TreatingProviderListCtrl", function($scope, $rootScope, $state, $stateParams, TreatingProviderService, Utils, GeneralUiGrid) {
    $scope.loadingGrid = false;
    $scope.sortingOptions = null;
    $scope.filteringOptions = [];
    $scope.paginationOptions = {
        page: 1,
    };
    $scope.getDisplayType = function(type) {
        var choice = $global.typeChoices.filter(function(v) {
            return v.value==type
        })[0];
        return choice? choice.display_name: type;
    };

    if (!$rootScope.$global.TreatingProvider) {
        $rootScope.$global.TreatingProvider = {}
    }

    var initialized = true,
        $global = $rootScope.$global.TreatingProvider;
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
                }
            ],
            // onRegisterApi: GeneralUiGrid.onRegisterApi($scope)
        };
    }
    $global.gridOptions.onRegisterApi = GeneralUiGrid.onRegisterApi($scope);
    $scope.getPage = GeneralUiGrid.getPage($scope, TreatingProviderService, $global.gridOptions);
    if (!initialized) {
        $scope.getPage();
    }

});

app.controller("TreatingProviderNewCtrl", function($scope, $rootScope, $state,$stateParams, TreatingProviderService, Utils) {
    var $global = $rootScope.$global.TreatingProvider;
    $scope.selectedRecord = new TreatingProviderService();
    $scope.addRecord = function() {
        $scope.saving = true;
        $scope.selectedRecord.$save().then(function(response) {
            if ($global && $global.gridOptions) {
                $global.gridOptions.data.splice(0, 0, response);
            }
            $rootScope.$global.TreatingProvider.comboData = undefined;
            $state.go('treating_provider-list');
            Utils.showDefaultServerSuccess(response);
        }, function(response) {
            Utils.showDefaultServerError(response);
        }).finally(function() {
            $scope.saving = false;
        });
    };
});

app.controller("TreatingProviderEditCtrl", function($scope, $rootScope, $state,$stateParams, TreatingProviderService, Utils, $uibModal) {
    var $global = $rootScope.$global.TreatingProvider;

    $scope.showDeleteConfirm = function() {
        if (!$scope.selectedRecord) {
            return;
        }
        var id = $scope.selectedRecord.id;
        var $global = $rootScope.$global.TreatingProvider;
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
                        $rootScope.$global.TreatingProvider.comboData = undefined;
                        Utils.showDefaultServerSuccess(response);
                        $uibModalInstance.close();
                        $state.go('treating_provider-list');
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
            $rootScope.$global.TreatingProvider.comboData = undefined;
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

app.controller("PatientVisitListCtrl", function($scope, $rootScope, $state, $stateParams, PatientVisitService, Utils, GeneralUiGrid) {
    $scope.loadingGrid = false;
    $scope.sortingOptions = null;
    $scope.filteringOptions = [];
    $scope.paginationOptions = {
        page: 1,
    };
    if (!$rootScope.$global.PatientVisit) {
        $rootScope.$global.PatientVisit = {}
    }

    var initialized = true,
        $global = $rootScope.$global.PatientVisit;
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
                {name: 'referring_entity', 'displayName': 'Referring Entity',
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope"><a class="text text-primary" href="{{grid.appScope.$state.href(\'patient_visit-edit\', {id: row.entity.id})}}">{{row.entity._referring_entity.entity_name}}</a></div>'
                },
                {name: 'treating_provider', 'displayName': 'Treating Provider',
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope">{{row.entity._treating_provider.provider_name}}</div>'
                },
                {name: 'visit_date', 'displayName': 'Visit Date', width: 120,
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope">{{row.entity.visit_date|date: \'MMM dd, yyyy\'}}</div>'
                },
                {name: 'visit_appointment_time', 'displayName': 'App. Time', width: 120,
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope">{{row.entity.visit_appointment_time|date: \'hh:mm a\'}}</div>'
                },
                {name: 'visit_actual_time', 'displayName': 'Actual Time', width: 120,
                    cellTemplate: '<div class="ui-grid-cell-contents ng-binding ng-scope">{{row.entity.visit_actual_time|date: \'hh:mm a\'}}</div>'
                },
                {name: 'visit_count', 'displayName': 'Visit Count', width: 120}
            ],
            // onRegisterApi: GeneralUiGrid.onRegisterApi($scope)
        };
    }
    $global.gridOptions.onRegisterApi = GeneralUiGrid.onRegisterApi($scope);
    $scope.getPage = GeneralUiGrid.getPage($scope, PatientVisitService, $global.gridOptions);
    if (!initialized) {
        $scope.getPage();
    }
});

app.controller("PatientVisitNewCtrl", function($scope, $rootScope, $state,$stateParams, PatientVisitService, ReferringEntityService, TreatingProviderService, Utils) {
    var $global = $rootScope.$global.PatientVisit;
    $scope.selectedRecord = new PatientVisitService();
    $rootScope.loadReferringEntityCombo();
    $rootScope.loadTreatingProviderCombo();
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

app.controller("PatientVisitEditCtrl", function($scope, $rootScope, $state,$stateParams, PatientVisitService, ReferringEntityService, TreatingProviderService, Utils, $uibModal) {
    var $global = $rootScope.$global.PatientVisit;
    $rootScope.loadReferringEntityCombo();
    $rootScope.loadTreatingProviderCombo();

    $scope.showDeleteConfirm = function() {
        if (!$scope.selectedRecord) {
            return;
        }
        var id = $scope.selectedRecord.id;
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
                        $state.go('patient_visit-list');
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


/******************************************************************
********************* PatientVisitsReport controllers *****************
*******************************************************************/

app.controller("PatientVisitsReportCtrl", function($scope, $rootScope, $http, $state, $stateParams, Utils) {
    var $global = $rootScope.$global.PatientVisitsReport
    updateTotal = function() {
        $global.total = {};
        angular.forEach($global.tableData, function(org) {
            angular.forEach(org.counts, function(c, k) {
                if ($global.total[k] == undefined) {
                    $global.total[k] = 0;
                }
                $global.total[k] += c;
            });
        });
    };
    $scope.refreshData = function() {
        var lastYear = moment().year() - 1;
        $global.today = moment().toDate();
        $global.yesterday = moment().add(-1, 'days').toDate();
        $global.mtdRange = [moment().date(1).toDate(), moment().toDate()];
        $global.mtdLastRange = [moment().date(1).year(lastYear).toDate(), moment().year(lastYear).toDate()];
        $global.ytdRange = [moment().date(1).month(0).toDate(), moment().toDate()];
        $global.ytdLastRange = [moment().date(1).month(0).year(lastYear).toDate(), moment().year(lastYear).toDate()];

        $global.refreshing = true;
        $http.get("/api/v1/report/patient_visits").
        then(function(response) {
            $global.tableData = response.data;
            updateTotal();
        }, function(response) {
            Utils.showDefaultServerError(response);
        }).finally(function () {
            $global.refreshing = false;
        });
    };
    if ($global.tableData == undefined) {
        $scope.refreshData();
    }

});
