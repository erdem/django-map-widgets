DjangoMapWidgetGenerater = $.Class.extend({

    init: function (options) {
        $.extend(this, options);
        $(document).on("click", this.inline_add_row_jquery_selector, this.handleInlineAddRowBtn.bind(this));

    },

    getWidgetData: function () {

    },

    handleInlineAddRowBtn: function (e) {

        var mapOptions = this.mapOptions;
        var widgetData = this.getWidgetData();

        // var wrapElemSelector = widgetData.wrapElemSelector;
        // var mapElemID = widgetData.mapElemID;
        // var googleAutoInputID = widgetData.googleAutoInputID;
        // var locationInputID = widgetData.locationInputID;
        //
        // var mapWidgetOptions = {
        //     locationInput: $(locationInputID),
        //     wrapElemSelector: wrapElemSelector,
        //     locationFieldValue: JSON.parse("{{ field_value|escapejs }}"),
        //     mapApiKey: null,
        //     mapElement: document.getElementById(mapElemID),
        //     mapCenterLocationName: mapOptions.mapCenterLocationName,
        //     mapCenterLocation: mapOptions.mapCenterLocation,
        //     coordinatesOverlayToggleBtn: $(".mw-btn-coordinates", wrapElemSelector),
        //     coordinatesOverlayDoneBtn: $(".mw-btn-coordinates-done", wrapElemSelector),
        //     coordinatesOverlayInputs: $(".mw-overlay-input", wrapElemSelector),
        //     coordinatesOverlay: $(".mw-coordinates-overlay", wrapElemSelector),
        //     myLocationBtn: $(".mw-btn-my-location", wrapElemSelector),
        //     addressAutoCompleteInput: document.getElementById(googleAutoInputID),
        //     deleteBtn: $(".mw-btn-delete", wrapElemSelector),
        //     addMarkerBtn: $(".mw-btn-add-marker", wrapElemSelector),
        //     loaderOverlayElem: $(".mw-loader-overlay", wrapElemSelector),
        //     zoom: mapOptions.zoom
        // };
        // new DjangoGoogleMapWidget(mapWidgetOptions);
    }
});


