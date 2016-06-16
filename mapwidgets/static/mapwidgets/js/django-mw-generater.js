(function($) {
    DjangoMapWidgetGenerater = $.Class.extend({

        init: function (options) {
            $.extend(this, options);
            $(document).on('formset:added', this.handle_added_formset_row.bind(this));

        },

        getWidgetData: function () {

        },

        handle_added_formset_row: function (e) {

            var mapOptions = this.mapOptions;
            var widgetData = this.getWidgetData();

        }
    });
})(jQuery || django.jQuery);

