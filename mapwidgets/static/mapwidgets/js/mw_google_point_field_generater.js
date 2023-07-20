(function($) {
    DjangoMapWidgetGenerater = $.Class.extend({

        init: function (options) {
            $.extend(this, options);
            $(document).on('formset:added', this.handle_added_formset_row.bind(this));
        },

        handle_added_formset_row: function (e, row, prefix) {
            var mapOptions = this.mapOptions;
            var widgetData = {};

            prefix = prefix || $(e.target).attr("id").split("-")[0];
            var id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");

            row = row || e.target;
            var numberPattern = /\d+/g;
            var row_index = $(row).attr("id").match(numberPattern);
            var replacement = prefix + "-" + row_index;
            $.each(this.widgetDataTemplate, function (key, value) {
                widgetData[key] = value.replace(id_regex, replacement)
            });

            var wrapElemSelector = widgetData.wrapElemSelector;
            var mapElemID = widgetData.mapElemID;
            var googleAutoInputID = widgetData.googleAutoInputID;
            var locationInputID = widgetData.locationInputID;

            var mapWidgetOptions = {
                locationInput: $(locationInputID),
                wrapElemSelector: wrapElemSelector,
                locationFieldValue: this.fieldValue,
                mapApiKey: null,
                mapElement: document.getElementById(mapElemID),
                mapCenterLocationName: mapOptions.mapCenterLocationName,
                mapCenterLocation: mapOptions.mapCenterLocation,
                coordinatesOverlayToggleBtn: $(".mw-btn-coordinates", wrapElemSelector),
                coordinatesOverlayDoneBtn: $(".mw-btn-coordinates-done", wrapElemSelector),
                coordinatesOverlayInputs: $(".mw-overlay-input", wrapElemSelector),
                coordinatesOverlay: $(".mw-coordinates-overlay", wrapElemSelector),
                myLocationBtn: $(".mw-btn-my-location", wrapElemSelector),
                addressAutoCompleteInput: document.getElementById(googleAutoInputID),
                deleteBtn: $(".mw-btn-delete", wrapElemSelector),
                addMarkerBtn: $(".mw-btn-add-marker", wrapElemSelector),
                loaderOverlayElem: $(".mw-loader-overlay", wrapElemSelector),
                zoom: mapOptions.zoom,
                markerFitZoom: mapOptions.markerFitZoom,
                GooglePlaceAutocompleteOptions: mapOptions.GooglePlaceAutocompleteOptions,
                markerCreateTriggerNameSpace: "google_point_map_widget:marker_create",
                markerChangeTriggerNameSpace: "google_point_map_widget:marker_change",
                markerDeleteTriggerNameSpace: "google_point_map_widget:marker_delete",
                placeChangedTriggerNameSpace: "google_point_map_widget:place_changed"
            };
            new DjangoGooglePointFieldWidget(mapWidgetOptions);
        }
    });
})(mapWidgets.jQuery);

