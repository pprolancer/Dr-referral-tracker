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
        showReason = showReason != undefined? showReason: true;
        if (response.status <= 0) {
            msg = "<strong>Server Connection Error</strong>";
        } else if(response.status == 401) {
            msg = "<strong>Session is expired.</strong> <br>You are redirecting to login page ...";
            var next = window.location.pathname+window.location.hash;
            setTimeout(function() {
                window.location = '/?next=' + next;
            }, 2000)
        } else {
            msg = "<strong>"+response.status + ": " + response.statusText + "</strong>";
            if (showReason && response.data) {
                msg += '<p>'+ this.prettyfiy_error(response.data) + '</p>';
            }
            if (extra_message) {
                msg += '<p>'+extra_message+'</p>';
            }
        }
        this.showError(msg, delay);
    };
    this.prettyfiy_error = function(data) {
        return JSON.stringify(data).replace(",", "<br>").replace(/\[|\]|\}|\{/g, "");
    }
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
    this.findByProperty = function(array, property, value) {
        for (var i = 0; i < array.length; i++) {
            if (array[i][property] == value) {
                return i;
            }
        }
        return -1;
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

app.factory('ReferringEntityService', ['$resource', function($resource) {
    return $resource('/api/v1/referring_entity/:id', {id: '@id'}, {
        update: {
            method: 'PUT'
        },
        'query': {
            method:'GET', isArray: false
        }
    });
}]);

app.factory('TreatingProviderService', ['$resource', function($resource) {
    return $resource('/api/v1/treating_provider/:id', {id: '@id'}, {
        update: {
            method: 'PUT'
        },
        'query': {
            method:'GET', isArray: false
        }
    });
}]);

app.factory('PatientVisitService', ['$resource', function($resource) {
    var _transferDateRequest = function(d) {
        return d && moment(d).format("YYYY-MM-DD");
    };
    var _transferTimeRequest = function(t) {
        return t && moment(t).format("HH:mm:ss");
    };
    var _transferDateResponse = function(d) {
        return d && moment(d+"T00:00:00Z").toDate();
    };
    var _transferTimeResponse = function(t) {
        return t && moment(moment().format("YYYY-MM-DD")+"T"+t).toDate();
    };
    var generalTransformRequest = function(data) {
        data.visit_date = _transferDateRequest(data.visit_date);
        data.visit_appointment_time = _transferTimeRequest(data.visit_appointment_time);
        data.visit_actual_time = _transferTimeRequest(data.visit_actual_time);
        return angular.toJson(data);

    };
    var generalTransformResponse = function (data) {
        var jdata = angular.fromJson(data)
        jdata.visit_date = _transferDateResponse(jdata.visit_date);
        jdata.visit_appointment_time = _transferTimeResponse(jdata.visit_appointment_time);
        jdata.visit_actual_time = _transferTimeResponse(jdata.visit_actual_time);
        return jdata;
    };

    return $resource('/api/v1/patient_visit/:id', {id: '@id'}, {
        update: {
            method: 'PUT',
            transformRequest: generalTransformRequest,
            transformResponse: generalTransformResponse
        },
        save: {
            method: 'POST',
            transformRequest: generalTransformRequest,
            transformResponse: generalTransformResponse
        },
        'query': {
            method:'GET', isArray: false,
            transformResponse: function(data) {
                var jdata = angular.fromJson(data)
                jdata.results.forEach(function(o) {
                    o.visit_date = _transferDateResponse(o.visit_date);
                    o.visit_appointment_time = _transferTimeResponse(o.visit_appointment_time);
                    o.visit_actual_time = _transferTimeResponse(o.visit_actual_time);
                });
                return jdata;
            }
        },
        get: {
            method: 'GET',
            params: {id: '@id'},
            transformResponse: generalTransformResponse
        },
    });
}]);
