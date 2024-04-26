(function($) {
    DjangoGooglePointFieldWidget = DjangoMapWidgetBase.extend({

        setMapOptions: async function (){
            this.mapInitializeOptions = {
                mapId: this.mapId,
                zoomControlOptions: {
                    position: google.maps.ControlPosition.RIGHT
                },
            }
            this.mapInitializeOptions = $.extend({}, this.mapInitializeOptions, this.mapOptions);
            let mapCenter = this.mapInitializeOptions.center
            if (!(mapCenter instanceof google.maps.LatLng) && Array.isArray(mapCenter)){
                mapCenter = new google.maps.LatLng(mapCenter[0], mapCenter[1]);
            }
            if (this.mapCenterLocationName) {
                try {
                    const response = await new Promise((resolve, reject) => {
                        this.geocoder.geocode({ 'address': this.mapCenterLocationName }, (results, status) => {
                            if (status === google.maps.GeocoderStatus.OK) {
                                resolve(results);
                            } else {
                                reject(status);
                            }
                        });
                    });
                    const geo_location = response[0].geometry.location;
                    mapCenter = new google.maps.LatLng(geo_location.lat(), geo_location.lng());
                } catch (error) {
                    console.error('Geocode lookup failed for `mapCenterLocationName` option:', error);
                }
            }
            this.mapInitializeOptions["center"] = mapCenter
        },

        initializeMap: async function(){
            this.geocoder = new google.maps.Geocoder();
            await this.setMapOptions();
            this.map = new google.maps.Map(this.mapElement, this.mapInitializeOptions);
            if (!$.isEmptyObject(this.djangoGeoJSONValue)){
                this.addMarkerToMap(this.djangoGeoJSONValue.lat, this.djangoGeoJSONValue.lng)
                this.updateDjangoInput();
                this.fitBoundMarker();
            }
            this.initializePlaceAutocomplete()
            $(this.mapElement).data('googlePointFieldMapObj', this.map);
            $(this.mapElement).data('googlePointFieldObj', this);
        },

        initializePlaceAutocomplete: function (){
            this.autocomplete = new google.maps.places.Autocomplete(this.addressAutoCompleteInput, this.GooglePlaceAutocompleteOptions);
            this.autocomplete.bindTo("bounds", this.map);
            this.autocomplete.addListener("place_changed", this.handleAutoCompletePlaceChange.bind(this, this.autocomplete));
            this.addressAutoCompleteInput.addEventListener('keydown', this.handleAutoCompleteInputKeyDown.bind(this));
        },

        addMarkerToMap: function(lat, lng){
            this.removeMarker();
            const marker_position = {lat: parseFloat(lat), lng: parseFloat(lng)};
            this.marker = new google.maps.marker.AdvancedMarkerElement({
                map: this.map,
                position: marker_position,
                gmpDraggable: true
            });
            this.marker.addListener("dragend", this.dragMarker.bind(this));
        },

        serializeMarkerToGeoJSON: function(){
            if (this.marker){
                const position = this.marker.position;
                return {
                    type: "Point",
                    coordinates: [position.lng, position.lat]
                };
            }
        },

        fitBoundMarker: function () {
            const bounds = new google.maps.LatLngBounds();
            bounds.extend(this.marker.position);
            this.map.fitBounds(bounds);
            if (this.markerFitZoom && this.isInt(this.markerFitZoom)){
                const markerFitZoom = parseInt(this.markerFitZoom);
                const listener = google.maps.event.addListener(this.map, "idle", function() {
                    if (this.getZoom() > markerFitZoom) {
                        this.setZoom(markerFitZoom)
                    }
                    google.maps.event.removeListener(listener);
                });
            }
        },

        removeMarker: function(e){
            if (this.marker){
                this.marker.setMap(null);
            }
            this.marker = null;
        },

        dragMarker: function(e){
            this.addMarkerToMap(e.latLng.lat(), e.latLng.lng())
            this.updateDjangoInput()
        },

        handleAutoCompletePlaceChange: function (autocomplete) {
            const place = autocomplete.getPlace();
            if (!place.geometry) {
                // User entered the name of a Place that was not suggested and
                // pressed the Enter key, or the Place Details request failed.
                return;
            }
            const lat = place.geometry.location.lat();
            const lng = place.geometry.location.lng();
            this.addMarkerToMap(lat, lng);
            this.updateDjangoInput(place);
            this.fitBoundMarker()
        },

        handleAutoCompleteInputKeyDown: function (e) {
            const keyCode = e.keyCode || e.which;
            if (keyCode === 13){  // pressed enter key
                e.preventDefault();
                return false;
            }
        },

        handleAddMarkerBtnClick: function(e){
            $(this.mapElement).toggleClass("click");
            this.addMarkerBtn.toggleClass("active");
            if ($(this.addMarkerBtn).hasClass("active")){
                this.map.addListener("click", this.handleMapClick.bind(this));
            }else{
                google.maps.event.clearListeners(this.map, 'click');
            }
        },

        handleMapClick: function(e){
            google.maps.event.clearListeners(this.map, 'click');
            $(this.mapElement).removeClass("click");
            this.addMarkerBtn.removeClass("active");
            this.addMarkerToMap(e.latLng.lat(), e.latLng.lng())
            this.updateDjangoInput()
        }
    });

})(mapWidgets.jQuery);
