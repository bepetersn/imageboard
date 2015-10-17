
// Define an "app" module that can be used to
// create an initial set of views.


Imageboard = (function() {

	var AppView = Backbone.View.extend({
		render: function(){
			console.log('in render');
			return this;
		}
	});

    return {
        init: function() {
            console.log('in init');
            var appView = new AppView();
            appView.render();
        }
    };
})();
