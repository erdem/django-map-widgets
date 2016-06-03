$.namespace("DjangoInlineGoogleMapWidget");


DjangoInlineGoogleMapWidget = DjangoGoogleMapWidget.extend({

    init: function (options) {
        $.extend(this, options);
        this.Super();
        setTimeout(function () {
            this.addInlineRowBtn = $(this.eee, "body");
            console.log(this.addInlineRowBtn)
            this.addInlineRowBtn.on("click", this.handleaddInlineRowBtnClick.bind(this));
        }.bind(this), 500);
    },

    handleaddInlineRowBtnClick: function (e) {
        alert("asd");
    }
});