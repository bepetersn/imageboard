
// Define an "app" module that can be used to
// create an initial set of views.


Imageboard = (function() {
    return {
        init: function() {
            console.log('in init');
            appView = AppView();
            appView.render();
        }
    };
})();
