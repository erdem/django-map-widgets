$.namespace("DjangoMapWidgetGenerater");

DjangoMapWidgetGenerater = $.Class.extend({

    init: function (options) {
        $.extend(this, options);
        console.log("initialize");
        $(document).on("click", this.inline_add_row_jquery_selector, this.handleInlineAddRowBtn.bind(this));
    },

    handleInlineAddRowBtn: function (e) {
        console.log("click!");
    }
});


