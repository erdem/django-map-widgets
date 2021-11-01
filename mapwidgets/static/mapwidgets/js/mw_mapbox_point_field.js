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
    
          // For the geocoding etc.
          mapboxgl.accessToken = this.mapOptions.access_token;

          this.mapboxSDK = new mapboxSdk({ accessToken: this.mapOptions.access_token });

          this.geocoder = new MapboxGeocoder({
            accessToken: mapboxgl.accessToken,
            zoom: 13,
            placeholder: 'Search a location',
            mapboxgl: mapboxgl,
            reverseGeocode: true,
            marker: false
          })

          this.geocoder.on('result', (place) => this.handleAutoCompletePlaceChange(place.result))

          this.initializeMap.bind(this)();
        },

        initializeMap: function(){
            var mapCenter = this.mapCenterLocation;
            this.map = new mapboxgl.Map({
                container: this.mapElement.id, // container ID
                style: 'mapbox://styles/mapbox/streets-v11', // style URL
                center: [mapCenter[1], mapCenter[0]], // starting position [lng, lat]
                zoom: this.zoom // starting zoom
            });

            this.geocoder.addTo(this.map)
            
            $(this.mapElement).data('mapbox_map', this.map);
            $(this.mapElement).data('mapbox_map_widget', this);

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
            this.map.flyTo({
              center: this.marker.getLngLat(),
              zoom: 14
            });
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
            })
              .send()
              .then(response => {
                const address = response?.body?.features?.[0];
                this.geocoder.clear();
                this.geocoder.setPlaceholder(address?.place_name || "Somewhere");
                $(document).trigger(this.placeChangedTriggerNameSpace,
                  [address, lat, lng, this.wrapElemSelector, this.locationInput]
                )
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
        },
    });

})(mapWidgets.jQuery);
