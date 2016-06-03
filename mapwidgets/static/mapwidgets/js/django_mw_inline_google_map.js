$.namespace("DjangoInlineGoogleMapWidget");


DjangoInlineGoogleMapWidget = DjangoGoogleMapWidget.extend({

    init: function (options) {
        $.extend(this, options);
        this.Super()
    }
});