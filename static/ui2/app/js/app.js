var app = angular.module("drReferral", ['ui.router', 'ngResource', 'ngAnimate', 'ui.bootstrap', 'ui.grid', 'ui.grid.pagination']);

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
