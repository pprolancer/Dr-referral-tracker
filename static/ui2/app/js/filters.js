// Source: dist/.temp/filters/default/default.js
app.filter('default', function () {
    return function (input, value) {
        if (input !== null && input !== undefined && input !== '') {
            return input;
        }
        return value || '';
    };
});

app.filter('orderObjectBy', function() {
    return function(items, field, reverse) {
        var filtered = [];
        angular.forEach(items, function(item) {
            filtered.push(item);
        });
        filtered.sort(function (a, b) {
            return (a[field] > b[field] ? 1 : -1);
        });
        if(reverse) filtered.reverse();
        return filtered;
    };
});


app.filter('sumByKey', function() {
    return function(items, prop) {
        if (typeof(items) === 'undefined' || typeof(prop) === 'undefined') {
            return 0;
        }
        return items.reduce( function(a, b) {
            return a + b[prop];
        }, 0);
    };
});
