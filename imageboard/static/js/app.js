
// Define an "app" module that can be used to
// create an initial set of views.


Imageboard = (function() {

	var AppView = Backbone.View.extend({

		render: function(){
			console.log('in render');
			this.$el.append('Hello backbone');
			return this;
		}
	});

    return {
        init: function() {
            console.log('in init');
            var appView = new AppView({
                el: '#content'
            });
            appView.render();
        }
    };

})();
