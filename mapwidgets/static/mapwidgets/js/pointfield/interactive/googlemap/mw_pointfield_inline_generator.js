(function ($) {
    DjangoMapWidgetGenerator = $.Class.extend({

        init: function (options) {
            $.extend(this, options);
            $(document).on('formset:added', this.handle_added_formset_row.bind(this));
        },

        handle_added_formset_row: function (e, row, prefix) {
            prefix = prefix || $(e.target).attr("id").split("-")[0];

            row = row || e.target;
            const id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");
            const numberPattern = /\d+/g;
            const row_index = $(row).attr("id").match(numberPattern);
            const replacement = prefix + "-" + row_index;
            let widgetData = {};
            $.each(this.widgetDataTemplate, function (key, value) {
                widgetData[key] = value.replace(id_regex, replacement)
            });

            const widgetWrapSelector = widgetData.widgetWrapSelector;
            const mapId = widgetData.mapId;
            const googleAutoInputId = widgetData.googleAutoInputId;
            const djangoInputId = widgetData.djangoInputId;

            const mapWidgetOptions = {
                mapId: mapId,
                djangoInput: $(djangoInputId),
                wrapElemSelector: widgetWrapSelector,
                mapElement: document.getElementById(mapId),
                coordinatesOverlayToggleBtn: $(".mw-btn-coordinates", widgetWrapSelector),
                coordinatesOverlayDoneBtn: $(".mw-btn-coordinates-done", widgetWrapSelector),
                coordinatesOverlayInputs: $(".mw-overlay-input", widgetWrapSelector),
                coordinatesOverlay: $(".mw-coordinates-overlay", widgetWrapSelector),
                myLocationBtn: $(".mw-btn-my-location", widgetWrapSelector),
                addressAutoCompleteInput: document.getElementById(googleAutoInputId),
                deleteBtn: $(".mw-btn-delete", widgetWrapSelector),
                addMarkerBtn: $(".mw-btn-add-marker", widgetWrapSelector),
                loaderOverlayElem: $(".mw-loader-overlay", widgetWrapSelector),
                mapOptions: this.widgetSettings.mapOptions,
                mapCenterLocationName: this.widgetSettings.mapCenterLocationName,
                markerFitZoom: this.widgetSettings.markerFitZoom,
                GooglePlaceAutocompleteOptions: this.widgetSettings.GooglePlaceAutocompleteOptions,
                markerCreateTriggerNameSpace: "googleMapPointFieldWidget:markerCreate",
                markerChangeTriggerNameSpace: "googleMapPointFieldWidget:markerChange",
                markerDeleteTriggerNameSpace: "googleMapPointFieldWidget:markerDelete",
                placeChangedTriggerNameSpace: "googleMapPointFieldWidget:placeChanged"
            };
            new DjangoGooglePointFieldWidget(mapWidgetOptions);
        }
    });
})(mapWidgets.jQuery);

