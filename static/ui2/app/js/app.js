var app = angular.module("drReferral", ['ui.router', 'ui.grid', 'ui.grid.pagination']);

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
        url: "/organization-list",
        templateUrl : 'app/partials/pages/organization/list.html',
        data: {
            pageInfo: {
                title: 'Organization',
                titleDesc: 'list of organizations'
            }
        },
        controller  : 'OrganizationCtrl'
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

app.utils = {
    showMessage: function(msg, type, delay) {
        $.bootstrapGrowl(msg, {
          ele: 'body', // which element to append to
          type: type || 'info', // (null, 'info', 'danger', 'success')
          offset: {from: 'top', amount: 20}, // 'top', or 'bottom'
          align: 'center', // ('left', 'right', or 'center')
          width: 'auto', // (integer, or 'auto')
          delay: delay != undefined? delay: 5000, // Time while the message will be displayed. It's not equivalent to the *demo* timeOut!
          allow_dismiss: true, // If true then will display a cross to close the popup.
          stackup_spacing: 10 // spacing between consecutively stacked growls.
        });
    },
    showSuccess: function(msg, delay) {
        app.utils.showMessage(msg, 'success', delay)
    },
    showError: function(msg, delay) {
        app.utils.showMessage(msg, 'danger', delay)
    },
    showWarn: function(msg, delay) {
        app.utils.showMessage(msg, 'warning', delay)
    },
    showDefaultServerSuccess: function(response, delay) {
        var delay = delay != undefined? delay: 5000;
        app.utils.showSuccess(response.statusText, delay);
    },
    showDefaultServerError: function(response, showReason, delay, extra_message) {
        var msg;
        delay = delay != undefined? delay: 5000;
        if (response.status <= 0) {
            msg = "Server Connection Error";
        } else if(response.status == 401) {
            msg = "Session is expired. you are redirecting to login page ...";
            window.location = '/login';
        } else {
            msg = response.status + ": " + response.statusText;
            if (showReason && response.responseJSON && response.responseJSON.reason) {
                msg += ' ('+ JSON.stringify(response.responseJSON.reason) + ')';
            }
            if (extra_message) {
                msg += extra_message;
            }
        }
        app.utils.showError(msg, delay);
    },
    random_id: function(n) {
        n = n || 10;
        return Math.floor((Math.random() * Math.pow(10, n)) + 1);
    },
    addQSParm: function(url, name, value) {
        var re = new RegExp("([?&]" + name + "=)[^&]+", "");

        function add(sep) {
            url += sep + name + "=" + encodeURIComponent(value);
        }

        function change() {
            url = url.replace(re, "$1" + encodeURIComponent(value));
        }
        if (url.indexOf("?") === -1) {
            add("?");
        } else {
            if (re.test(url)) {
                change();
            } else {
                add("&");
            }
        }
        return url;
    },
    noCacheUrl: function(url) {
        var r = app.utils.random_id();
        return app.utils.addQSParm(url, 'nc', r);
    }
};


/* Init global settings and run the app */
app.run(["$rootScope", "$state", function($rootScope, $state) {
    $rootScope.$state = $state; // state to be accessed from view
}]);
