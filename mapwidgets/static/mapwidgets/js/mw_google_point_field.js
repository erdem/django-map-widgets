(function($) {

    DjangoGooglePointFieldWidget = DjangoMapWidgetBase.extend({

        initializeWidget: function() {
            let mapCenter = this.mapCenterLocation;
            const handleGeocodeResults = (results, status) => {
                if (status === google.maps.GeocoderStatus.OK) {
                    const geoLocation = results[0].geometry.location;
                    mapCenter = [geoLocation.lat(), geoLocation.lng()];
                }
                this.initializeMap(mapCenter);
            };

            if (this.mapCenterLocationName) {
                this.geocoder.geocode({'address': this.mapCenterLocationName}, handleGeocodeResults.bind(this));
            } else {
                this.initializeMap(mapCenter);
            }
            $(this.mapElement).data('googleMapObj', this.map);
            $(this.mapElement).data('googleMapWidgetObj', this);
        },

        initializeMap: function(mapCenter) {
            this.map = new google.maps.Map(this.mapElement, {
                center: new google.maps.LatLng(mapCenter[0], mapCenter[1]),
                scrollwheel: this.scrollWheel,
                zoomControlOptions: {
                    position: google.maps.ControlPosition.RIGHT
                },
                zoom: this.zoom,
                streetViewControl: this.streetViewControl
            });

            if (!$.isEmptyObject(this.djangoGeoJSONValue)) {
                this.addMarkerToMap(this.djangoGeoJSONValue.lat, this.djangoGeoJSONValue.lng);
                this.updateDjangoInput();
                this.fitBoundMarker();
            }
        },

        addMarkerToMap: function(lat, lng) {
            this.removeMarker();
            const markerPosition = {lat: parseFloat(lat), lng: parseFloat(lng)};
            this.marker = new google.maps.Marker({
                position: markerPosition,
                map: this.map,
                draggable: true
            });
            this.marker.addEventListener("dragend", this.dragMarker.bind(this));
        },

        serializeMarkerToGeoJSON: function() {
            if (this.marker) {
                const position = this.marker.getPosition();
                return {
                    type: "Point",
                    coordinates: [position.lng(), position.lat()]
                };
            }
            return null;
        },

        fitBoundMarker: function() {
            const bounds = new google.maps.LatLngBounds();
            bounds.extend(this.marker.getPosition());
            this.map.fitBounds(bounds);
            if (this.markerFitZoom && this.isInt(this.markerFitZoom)) {
                const markerFitZoom = parseInt(this.markerFitZoom);
                const listener = google.maps.event.addEventListener(this.map, "idle", function() {
                    if (this.getZoom() > markerFitZoom) {
                        this.setZoom(markerFitZoom);
                    }
                    google.maps.event.removeListener(listener);
                });
            }
        },

        removeMarker: function() {
            if (this.marker) {
                this.marker.setMap(null);
            }
            this.marker = null;
        },

        dragMarker: function(e) {
            this.addMarkerToMap(e.latLng.lat(), e.latLng.lng());
            this.updateDjangoInput();
        },

        handleAddMarkerBtnClick: function() {
            $(this.mapElement).toggleClass("click");
            this.addMarkerBtn.toggleClass("active");
            if ($(this.addMarkerBtn).hasClass("active")) {
                this.map.addEventListener("click", this.handleMapClick.bind(this));
            } else {
                google.maps.event.clearListeners(this.map, 'click');
            }
        },

        handleMapClick: function(e) {
            $(this.mapElement).removeClass("click");
            this.addMarkerBtn.removeClass("active");
            this.addMarkerToMap(e.latLng.lat(), e.latLng.lng());
            this.updateDjangoInput();
        }
    });

})(mapWidgets.jQuery);
