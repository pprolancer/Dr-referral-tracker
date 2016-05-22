app.service('Utils', [function() {
    this.showMessage = function(msg, type, delay) {
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
    };
    this.showSuccess = function(msg, delay) {
        this.showMessage(msg, 'success', delay)
    };
    this.showError = function(msg, delay) {
        this.showMessage(msg, 'danger', delay)
    };
    this.showWarn = function(msg, delay) {
        this.showMessage(msg, 'warning', delay)
    };
    this.showDefaultServerSuccess = function(response, delay) {
        var delay = delay != undefined? delay: 5000,
            defaultMsg = 'Operation done successfully';
        this.showSuccess(response.statusText || defaultMsg, delay);
    };
    this.showDefaultServerError = function(response, showReason, delay, extra_message) {
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
        this.showError(msg, delay);
    };
    this.random_id = function(n) {
        n = n || 10;
        return Math.floor((Math.random() * Math.pow(10, n)) + 1);
    };
    this.addQSParm = function(url, name, value) {
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
    };
    this.noCacheUrl = function(url) {
        var r = this.random_id();
        return this.addQSParm(url, 'nc', r);
    };
}]);

app.factory('GeneralUiGrid', ['uiGridConstants', 'Utils', function(uiGridConstants, Utils) {
    return {
        onRegisterApi: function($scope) {
            return function(gridApi) {
                $scope.gridApi = gridApi;
                gridApi.core.on.sortChanged($scope, function(grid, sortColumns) {
                    if ($scope.loadingGrid) {
                        return;
                    }
                    if (sortColumns.length == 0) {
                        $scope.sortingOptions = null;
                    } else {
                        var col = sortColumns[0];
                        $scope.sortingOptions = (col.sort.direction==uiGridConstants.DESC?"-":"") + col.field;
                    }
                    $scope.getPage();
                });
                gridApi.pagination.on.paginationChanged($scope, function (newPage, pageSize) {
                    if ($scope.loadingGrid) {
                        return;
                    }
                    $scope.paginationOptions.page = newPage;
                    // $scope.paginationOptions.pageSize = pageSize;
                    $scope.getPage();
                });

            }
        },
        getPage: function($scope, queryService, gridOpt) {
            return function() {
                $scope.loadingGrid = true;
                var params = {page: $scope.paginationOptions.page};
                if ($scope.sortingOptions) {
                    params.ordering=$scope.sortingOptions;
                }
                queryService.query(params, function(response) {
                    var pg = response.pagination;
                    gridOpt.data = response.results;
                    gridOpt.totalItems = pg.count;
                    gridOpt.paginationCurrentPage = pg.current_page;
                    gridOpt.paginationPageSize = pg.page_size;
                }, function(response) {
                    Utils.showDefaultServerError(response);
                }).$promise.finally(function() {
                    $scope.loadingGrid = false;
                });
            }
        }
    };
}]);

app.factory('SessionService', ['$resource', function($resource) {
    return $resource('/api/v1/session/', {}, {
        'query': {
            method:'GET', isArray: false
        }
    });
}]);


app.factory('OrganizationService', ['$resource', function($resource) {
    return $resource('/api/v1/organization/:id', {id: '@id'}, {
        update: {
            method: 'PUT'
        },
        'query': {
            method:'GET', isArray: false
        }
    });
}]);
