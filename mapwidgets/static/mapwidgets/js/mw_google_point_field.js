(function($) {
    DjangoGooglePointFieldWidget = DjangoMapWidgetBase.extend({

        initializeMap: function(){
            let mapCenter = this.mapCenterLocation;
            this.geocoder = new google.maps.Geocoder();
            if (this.mapCenterLocationName){
                this.geocoder.geocode({'address' : this.mapCenterLocationName}, function(results, status) {
                    if (status === google.maps.GeocoderStatus.OK) {
                        const geo_location = results[0].geometry.location;
                        mapCenter = [geo_location.lat(), geo_location.lng()];
                    }
                    this.map = new google.maps.Map(this.mapElement, {
                        center: new google.maps.LatLng(mapCenter[0], mapCenter[1]),
                        mapId: this.mapId,
                        scrollwheel: this.scrollWheel,
                        zoomControlOptions: {
                            position: google.maps.ControlPosition.RIGHT
                        },
                        zoom: this.zoom,
                        streetViewControl: this.streetViewControl,
                    });

                    if (!$.isEmptyObject(this.djangoGeoJSONValue)){
                        this.addMarkerToMap(this.djangoGeoJSONValue.lat, this.djangoGeoJSONValue.lng)
                        this.updateDjangoInput();
                        this.fitBoundMarker();
                    }
                    this.initializePlaceAutocomplete()
                }.bind(this));
            }else{
                this.map = new google.maps.Map(this.mapElement, {
                    center: new google.maps.LatLng(mapCenter[0], mapCenter[1]),
                    scrollwheel: this.scrollWheel,
                    zoomControlOptions: {
                        position: google.maps.ControlPosition.RIGHT
                    },
                    zoom: this.zoom,
                    streetViewControl: this.streetViewControl,
                    mapId: this.mapId
                });

                if (!$.isEmptyObject(this.djangoGeoJSONValue)){
                    this.addMarkerToMap(this.djangoGeoJSONValue.lat, this.djangoGeoJSONValue.lng)
                    this.updateDjangoInput();
                    this.fitBoundMarker();
                }
                this.initializePlaceAutocomplete()
            }
            $(this.mapElement).data('googleMapObj', this.map);
            $(this.mapElement).data('googleMapWidgetObj', this);
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
                draggable: true
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
