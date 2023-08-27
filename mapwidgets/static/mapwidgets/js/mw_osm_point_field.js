(function($) {
    DjangoOSMPointFieldWidget = DjangoMapWidgetBase.extend({

        initializeMap: function() {
            let mapCenter = this.mapCenterLocation;
            this.map = L.map(this.mapElement).setView([mapCenter[0], mapCenter[1]], this.zoom);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(this.map);

            if (!$.isEmptyObject(this.locationFieldValue)) {
                this.updateLocationInput(this.locationFieldValue.lat, this.locationFieldValue.lng);
                this.fitBoundMarker();
            }

            $(this.mapElement).data('osmMapObj', this.map);
            $(this.mapElement).data('osmMapWidgetObj', this);
        },

        addMarkerToMap: function(lat, lng) {
            this.removeMarker();
            this.marker = L.marker([lat, lng], { draggable: true }).addTo(this.map);
            this.marker.on('dragend', this.dragMarker.bind(this));
        },

        fitBoundMarker: function() {
            var bounds = L.latLngBounds([this.marker.getLatLng()]);
            this.map.fitBounds(bounds);

            if (this.markerFitZoom && this.isInt(this.markerFitZoom)) {
                var markerFitZoom = parseInt(this.markerFitZoom);
                this.map.on('zoomend', function() {
                    if (this.map.getZoom() > markerFitZoom) {
                        this.map.setZoom(markerFitZoom);
                    }
                }.bind(this));
            }
        },

        removeMarker: function() {
            if (this.marker) {
                this.map.removeLayer(this.marker);
            }
        },

        dragMarker: function(e) {
            var latlng = e.target.getLatLng();
            this.updateLocationInput(latlng.lat, latlng.lng);
        },

        handleAddMarkerBtnClick: function() {
            $(this.mapElement).toggleClass("click");
            this.addMarkerBtn.toggleClass("active");

            if ($(this.addMarkerBtn).hasClass("active")) {
                this.map.on('click', this.handleMapClick.bind(this));
            } else {
                this.map.off('click');
            }
        },

        handleMapClick: function(e) {
            this.map.off('click');
            $(this.mapElement).removeClass("click");
            this.addMarkerBtn.removeClass("active");
            this.updateLocationInput(e.latlng.lat, e.latlng.lng);
        }
    });

})(mapWidgets.jQuery);
