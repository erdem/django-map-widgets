$.namespace("DjangoMapWidgetGenerater");

DjangoMapWidgetGenerater = $.Class.extend({

    init: function (options) {
        $.extend(this, options);
        $(document).on("click", ".add-row a", this.handleInlineAddRowBtn.bind(this));
    },

    handleInlineAddRowBtn: function (e) {
        console.log("click!");
    }
});

(function() {
    var django_mw_generate = new DjangoMapWidgetGenerater()
})();
