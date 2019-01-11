(function($) {
    DjangoMapWidgetGenerater = $.Class.extend({

        init: function (options) {
            $.extend(this, options);
            $(document).on('formset:added', this.handle_added_formset_row.bind(this));
        },

        handle_added_formset_row: function (e, row, prefix) {
            var mapOptions = this.mapOptions;
            var widgetData = {};

            var rowIdSelector = '#'+row[0].id
            var mapElemIdSelector = this.widgetDataTemplate.mapElemIDSelector;
            var elemIsInRow = document.querySelector(rowIdSelector + ' ' + mapElemIdSelector)

            if (!elemIsInRow) return;

            var row_id = $(row).attr("id")

            var wrapElemSelector = rowIdSelector + ' .mw-wrap';
            var mapElemID = rowIdSelector + ' ' + mapElemIdSelector;
            var googleAutoInputID = rowIdSelector + ' .mw-google-address-input';
            var locationInputID = rowIdSelector + ' .coordinates-input';

            var mapWidgetOptions = {
                locationInput: $(locationInputID),
                wrapElemSelector: wrapElemSelector,
                locationFieldValue: this.fieldValue,
                mapApiKey: null,
                mapElement: document.querySelector(mapElemID),
                mapCenterLocationName: mapOptions.mapCenterLocationName,
                mapCenterLocation: mapOptions.mapCenterLocation,
                coordinatesOverlayToggleBtn: $(".mw-btn-coordinates", wrapElemSelector),
                coordinatesOverlayDoneBtn: $(".mw-btn-coordinates-done", wrapElemSelector),
                coordinatesOverlayInputs: $(".mw-overlay-input", wrapElemSelector),
                coordinatesOverlay: $(".mw-coordinates-overlay", wrapElemSelector),
                myLocationBtn: $(".mw-btn-my-location", wrapElemSelector),
                addressAutoCompleteInput: document.querySelector(googleAutoInputID),
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
})(django.jQuery || jQuery);

