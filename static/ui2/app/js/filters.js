// Source: dist/.temp/filters/default/default.js
app.filter('default', function () {
    return function (input, value) {
        if (input !== null && input !== undefined && input !== '') {
            return input;
        }
        return value || '';
    };
});
