$.namespace("DjangoInlineGoogleMapWidget");


DjangoInlineGoogleMapWidget = DjangoGoogleMapWidget.extend({

    init: function (options) {
        $.extend(this, options);
        this.Super();
        // setTimeout(function () {
        //     console.log(this.addInlineRowBtn);
        //     $(this.addInlineRowBtn).on("click", this.handleaddInlineRowBtnClick.bind(this));
        // }.bind(this), 1500);
    },

    handleaddInlineRowBtnClick: function (e) {
        // e.preventDefault();
        console.log("asda");
    }
});