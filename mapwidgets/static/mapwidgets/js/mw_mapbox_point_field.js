(function($) {
    DjangoMapboxPointFieldWidget = DjangoMapWidgetBase.extend({

        init: function(options){
            $.extend(this, options);

            this.coordinatesOverlayToggleBtn.on("click", this.toggleCoordinatesOverlay.bind(this));
            this.coordinatesOverlayDoneBtn.on("click", this.handleCoordinatesOverlayDoneBtnClick.bind(this));
            this.coordinatesOverlayInputs.on("change", this.handleCoordinatesInputsChange.bind(this));
            this.addMarkerBtn.on("click", this.handleAddMarkerBtnClick.bind(this));
            this.myLocationBtn.on("click", this.handleMyLocationBtnClick.bind(this));
            this.deleteBtn.on("click", this.resetMap.bind(this));

            // if the the location field in a collapse on Django admin form, the map need to initialize again when the collapse open by user.
            if ($(this.wrapElemSelector).closest('.module.collapse').length){
                $(document).on('show.fieldset', this.initializeMap.bind(this));
            }

            // set mapbox access_token.
            mapboxgl.accessToken = this.mapOptions.access_token;
            this.mapboxSDK = new mapboxSdk({ accessToken: this.mapOptions.access_token });

            // transform map options
            this.mapboxOptions = this.mapOptions.mapOptions || {}
            this.mapboxOptions.container = this.mapElement.id

            // transform geocoder options
            this.geocoderOptions = this.mapOptions.geocoderOptions || {}
            this.geocoderOptions.mapboxgl = mapboxgl
            this.geocoderOptions.accessToken = mapboxgl.accessToken
            if (!this.geocoderOptions.placeholder){
                this.geocoderOptions.placeholder = this.geocoderInputPlaceholderText
            }
            this.geocoder = new MapboxGeocoder(this.geocoderOptions)

            if (this.mapboxOptions.center){
                this.mapboxOptions.center = [this.mapboxOptions.center[1], this.mapboxOptions.center[0]]
            }
            this.flyToEnabled = this.geocoderOptions.flyTo || false
            this.geocoder.on('result', (place) => this.handleAutoCompletePlaceChange(place.result))
            this.initializeMap.bind(this)();
        },

        initializeMap: function(){
            this.map = new mapboxgl.Map(this.mapboxOptions);
            document.getElementById(this.geocoderWrapID).appendChild(this.geocoder.onAdd(this.map));

            if(this.mapOptions.showZoomNavigation){
                this.map.addControl(new mapboxgl.NavigationControl());
            }
            this.addressAutoCompleteInput = $("input:first", "#"+this.geocoderWrapID)
            $(this.mapElement).data('mapboxMapObj', this.map);
            $(this.mapElement).data('mapboxMapWidgetObj', this);

            if (!$.isEmptyObject(this.locationFieldValue)){
                this.updateLocationInput(this.locationFieldValue.lat, this.locationFieldValue.lng);
                this.fitBoundMarker();
            }
        },

        addMarkerToMap: function(lat, lng){
            this.removeMarker();
            this.marker = new mapboxgl.Marker()
                .setLngLat([parseFloat(lng), parseFloat(lat)])
                .setDraggable(true)
                .addTo(this.map);
            this.marker.on("dragend", this.dragMarker.bind(this));
        },

        fitBoundMarker: function () {
            if (this.marker) {
                if (this.flyToEnabled){
                    this.map.flyTo({
                        center: this.marker.getLngLat(),
                        zoom: this.mapOptions.markerFitZoom || 14
                    });
                }else{
                    this.map.jumpTo({
                        center: this.marker.getLngLat(),
                        zoom: this.mapOptions.markerFitZoom || 14
                    });
                }
            }
        },

        removeMarker: function(e){
            if (this.marker){
                this.marker.remove()
            }
        },

        dragMarker: function(e){
            const position = this.marker.getLngLat()
            this.updateLocationInput(position.lat, position.lng)
        },

        handleAddMarkerBtnClick: function(e){
            $(this.mapElement).toggleClass("click");
            this.addMarkerBtn.toggleClass("active");
            if ($(this.addMarkerBtn).hasClass("active")){
                this.map.on("click", this.handleMapClick.bind(this));
            } else {
                this.map.off("click", this.handleMapClick.bind(this));
            }
        },

        handleMapClick: function(e){
            this.map.off("click", this.handleMapClick.bind(this));
            $(this.mapElement).removeClass("click");
            this.addMarkerBtn.removeClass("active");
            this.updateLocationInput(e.lngLat.lat, e.lngLat.lng)
        },

        callPlaceTriggerHandler: function (lat, lng, place) {
            if (place === undefined) {
                this.mapboxSDK.geocoding.reverseGeocode({
                    query: [parseFloat(lng), parseFloat(lat)]
                }).send().then(response => {
                    const address = response?.body?.features?.[0];
                    this.geocoder.clear();
                    const placeName = address?.place_name || "Unknown Place"
                    this.addressAutoCompleteInput.val(placeName);
                    $(document).trigger(this.placeChangedTriggerNameSpace,
                        [address, lat, lng, this.wrapElemSelector, this.locationInput]
                    )
                    if ($.isEmptyObject(this.locationFieldValue)){
                        $(document).trigger(this.markerCreateTriggerNameSpace,
                            [address, lat, lng, this.wrapElemSelector, this.locationInput]
                        );
                    }else{
                        $(document).trigger(this.markerChangeTriggerNameSpace,
                            [address, lat, lng, this.wrapElemSelector, this.locationInput]
                        );
                    }
                })
            } else {  // user entered an address
                $(document).trigger(this.placeChangedTriggerNameSpace,
                    [place, lat, lng, this.wrapElemSelector, this.locationInput]
                );
            }
        },

        handleAutoCompletePlaceChange: function (place) {
            if (!place.geometry) {
                // User entered the name of a Place that was not suggested and
                // pressed the Enter key, or the Place Details request failed.
                return;
            }
            var [lng, lat] = place.geometry.coordinates;
            this.updateLocationInput(lat, lng, place);
            this.fitBoundMarker()
        }
    });

})(mapWidgets.jQuery);
