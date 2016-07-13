var app = angular.module("drReferral", ['ui.router', 'ngResource', 'ngAnimate', 'ui.bootstrap', 'ui.grid', 'ui.grid.pagination', 'ui.select', 'ngSanitize']);

app.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise("/dashboard");
    $stateProvider
    .state('dashboard', {
        url: "/dashboard",
        templateUrl : 'app/partials/pages/dashboard.html',
        data: {
            pageInfo: {
                title: 'Dashboard',
                titleDesc: 'reports & statistics'
            }
        },
        controller  : 'DashboardCtrl'
    }).state('organization-list', {
        url: "/organization/list",
        templateUrl : 'app/partials/pages/organization/list.html',
        data: {
            pageInfo: {
                title: 'Organization',
                titleDesc: 'list of organizations'
            }
        },
        controller  : 'OrganizationListCtrl'
    }).state('organization-new', {
        url: "/organization/new",
        templateUrl : 'app/partials/pages/organization/new.html',
        data: {
            pageInfo: {
                title: 'New Organization',
                titleDesc: 'add a new organization',
                back: 'organization-list'
            }
        },
        controller  : 'OrganizationNewCtrl'
    }).state('organization-edit', {
        url: "/organization/:id/edit",
        templateUrl : 'app/partials/pages/organization/edit.html',
        data: {
            pageInfo: {
                title: 'Edit Organization',
                titleDesc: 'edit an existing organization',
                back: 'organization-list'
            }
        },
        controller  : 'OrganizationEditCtrl'
    }).state('referring_entity-list', {
        url: "/referring_entity/list",
        templateUrl : 'app/partials/pages/referring_entity/list.html',
        data: {
            pageInfo: {
                title: 'Referring Entity',
                titleDesc: 'list of referring entities'
            }
        },
        controller  : 'ReferringEntityListCtrl'
    }).state('referring_entity-new', {
        url: "/referring_entity/new",
        templateUrl : 'app/partials/pages/referring_entity/new.html',
        data: {
            pageInfo: {
                title: 'New Referring Entity',
                titleDesc: 'add a new referring_entity',
                back: 'referring_entity-list'
            }
        },
        controller  : 'ReferringEntityNewCtrl'
    }).state('referring_entity-edit', {
        url: "/referring_entity/:id/edit",
        templateUrl : 'app/partials/pages/referring_entity/edit.html',
        data: {
            pageInfo: {
                title: 'Edit Referring Entity',
                titleDesc: 'edit an existing referring_entity',
                back: 'referring_entity-list'
            }
        },
        controller  : 'ReferringEntityEditCtrl'
    }).state('treating_provider-list', {
        url: "/treating_provider/list",
        templateUrl : 'app/partials/pages/treating_provider/list.html',
        data: {
            pageInfo: {
                title: 'Treating Provider',
                titleDesc: 'list of treating providers'
            }
        },
        controller  : 'TreatingProviderListCtrl'
    }).state('treating_provider-new', {
        url: "/treating_provider/new",
        templateUrl : 'app/partials/pages/treating_provider/new.html',
        data: {
            pageInfo: {
                title: 'New Treating Provider',
                titleDesc: 'add a new treating_provider',
                back: 'treating_provider-list'
            }
        },
        controller  : 'TreatingProviderNewCtrl'
    }).state('treating_provider-edit', {
        url: "/treating_provider/:id/edit",
        templateUrl : 'app/partials/pages/treating_provider/edit.html',
        data: {
            pageInfo: {
                title: 'Edit Treating Provider',
                titleDesc: 'edit an existing treating_provider',
                back: 'treating_provider-list'
            }
        },
        controller  : 'TreatingProviderEditCtrl'
    }).state('patient_visit-list', {
        url: "/patient_visit/list",
        templateUrl : 'app/partials/pages/patient_visit/list.html',
        data: {
            pageInfo: {
                title: 'Patient Visit',
                titleDesc: 'list of treating providers'
            }
        },
        controller  : 'PatientVisitListCtrl'
    }).state('patient_visit-new', {
        url: "/patient_visit/new",
        templateUrl : 'app/partials/pages/patient_visit/new.html',
        data: {
            pageInfo: {
                title: 'New Patient Visit',
                titleDesc: 'add a new patient_visit',
                back: 'patient_visit-list'
            }
        },
        controller  : 'PatientVisitNewCtrl'
    }).state('patient_visit-edit', {
        url: "/patient_visit/:id/edit",
        templateUrl : 'app/partials/pages/patient_visit/edit.html',
        data: {
            pageInfo: {
                title: 'Edit Patient Visit',
                titleDesc: 'edit an existing patient_visit',
                back: 'patient_visit-list'
            }
        },
        controller  : 'PatientVisitEditCtrl'
    }).state('patient_visits_report', {
        url: "/reports/patient_visit/",
        templateUrl : 'app/partials/pages/reports/patient_visits.html',
        data: {
            pageInfo: {
                title: 'Patient Visits Report',
                titleDesc: 'report of patient visits summary'
            }
        },
        controller  : 'PatientVisitsReportCtrl'
    });
});

app.config(['$controllerProvider', '$httpProvider', function($controllerProvider, $httpProvider) {
    $controllerProvider.allowGlobals();

    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
    function getCookie(c_name) {
        if (document.cookie.length > 0)
        {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1)
            {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    }
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);


/* Init global settings and run the app */
app.run(["$rootScope", "$state", function($rootScope, $state) {
    $rootScope.$state = $state; // state to be accessed from view
    $rootScope.$global = {};
}]);
