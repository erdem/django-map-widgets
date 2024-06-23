(function ($) {
    DjangoLeafletPointFieldWidget = DjangoMapWidgetBase.extend({

        initializeMap: function () {
            this.leafletMapOptions = this.mapOptions.mapOptions || {}
            if (!this.leafletMapOptions.center) {
                this.leafletMapOptions.center = this.mapCenterLocation
            }
            this.leafletTileLayer = this.mapOptions.tileLayer
            this.map = L.map(this.mapElement.id, this.leafletMapOptions);
            L.tileLayer(this.leafletTileLayer.urlTemplate, this.leafletTileLayer.options).addTo(this.map);
            if (this.map.zoomControl) {
                this.map.zoomControl.setPosition('topright');
            }
            $(this.mapElement).data("mwMapObj", this.map);
            $(this.mapElement).data("mwClassObj", this);

            if (!$.isEmptyObject(this.djangoGeoJSONValue)) {
                this.addMarkerToMap(this.djangoGeoJSONValue.lat, this.djangoGeoJSONValue.lng);
                this.updateDjangoInput();
                this.fitBoundMarker();
            }
        },

        addMarkerToMap: function (lat, lng) {
            this.removeMarker();
            this.marker = L.marker([lat, lng], {draggable: true}).addTo(this.map);
            this.marker.on("dragend", this.dragMarker.bind(this));
        },

        serializeMarkerToGeoJSON: function () {
            if (this.marker) {
                const position = this.marker.getLatLng();
                return {
                    type: "Point",
                    coordinates: [position.lng, position.lat]
                };
            }
            return null;
        },

        fitBoundMarker: function () {
            if (this.marker) {
                this.map.setView(this.marker.getLatLng(), this.markerFitZoom || 14);
            }
        },

        updateDjangoInput: function (place) {
            const django_input_val = this.serializeMarkerToGeoJSON();
            const lng = django_input_val.coordinates[0];
            const lat = django_input_val.coordinates[1];
            this.djangoInput.val(JSON.stringify(django_input_val));
            this.updateUXCoordinatesInputs(lat, lng);
            this.djangoGeoJSONValue = {
                "lng": lng,
                "lat": lat
            };
            this.enableClearBtn();
        },

        removeMarker: function () {
            if (this.marker) {
                this.map.removeLayer(this.marker);
            }
            this.marker = null;
        },

        dragMarker: function (e) {
            const position = e.target.getLatLng();
            this.addMarkerToMap(position.lat, position.lng);
            this.updateDjangoInput();
        },

        handleAddMarkerBtnClick: function (e) {
            $(this.mapElement).toggleClass("click");
            this.addMarkerBtn.toggleClass("active");
            if ($(this.addMarkerBtn).hasClass("active")) {
                this.map.on("click", this.handleMapClick.bind(this));
            } else {
                this.map.off("click", this.handleMapClick.bind(this));
            }
        },

        handleMapClick: function (e) {
            this.map.off("click", this.handleMapClick.bind(this));
            $(this.mapElement).removeClass("click");
            this.addMarkerBtn.removeClass("active");
            this.addMarkerToMap(e.latlng.lat, e.latlng.lng);
            this.updateDjangoInput();
        }
    });

})(mapWidgets.jQuery);
