(function ($) {
    DjangoGooglePointFieldWidget = DjangoMapWidgetBase.extend({

        initializeMap: async function () {
            
            // Redefine setMapOptions inside initializeMap to create a new closure for each instance
            const setMapOptions = async () => {
                let mapInitializeOptions = {
                    mapId: this.mapId,
                    zoomControlOptions: {
                        position: google.maps.ControlPosition.RIGHT
                    },
                };

                // Log the initial mapOptions
                console.log('Initial mapOptions for instance', this.mapId, ':', this.mapOptions);

                mapInitializeOptions = $.extend({}, mapInitializeOptions, this.mapOptions);

                let mapCenter = mapInitializeOptions.center;
                if (!(mapCenter instanceof google.maps.LatLng) && Array.isArray(mapCenter)) {
                    mapCenter = new google.maps.LatLng(mapCenter[0], mapCenter[1]);
                }

                if (this.mapCenterLocationName) {
                    try {
                        const response = await new Promise((resolve, reject) => {
                            this.geocoder.geocode({'address': this.mapCenterLocationName}, (results, status) => {
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

                mapInitializeOptions["center"] = mapCenter;

                // Log the final mapInitializeOptions
                console.log('Final mapInitializeOptions for instance', this.mapId, ':', mapInitializeOptions);

                return mapInitializeOptions;
            };

            // Rest of the initializeMap function
            this.geocoder = new google.maps.Geocoder();
            const mapOptions = await setMapOptions();

            // Log the mapOptions returned by setMapOptions
            console.log('mapOptions returned by setMapOptions for instance', this.mapId, ':', mapOptions);

            this.map = new google.maps.Map(this.mapElement, mapOptions);

            if (!$.isEmptyObject(this.djangoGeoJSONValue)) {
                this.addMarkerToMap(this.djangoGeoJSONValue.lat, this.djangoGeoJSONValue.lng);
                this.updateDjangoInput();
                this.fitBoundMarker();
            }
            this.initializePlaceAutocomplete();
        },

        // Check for PlaceAutocompleteElement support and choose appropriate API
        isNewAutocompleteSupported: function() {
            return typeof google !== 'undefined' && 
                   google.maps && 
                   google.maps.places && 
                   google.maps.places.PlaceAutocompleteElement &&
                   this.useNewAutocomplete !== false; // Allow explicit opt-out
        },

        initializePlaceAutocomplete: function () {
            if (this.isNewAutocompleteSupported()) {
                this.initializeNewPlaceAutocomplete();
            } else {
                this.initializeLegacyPlaceAutocomplete();
            }
        },

        initializeNewPlaceAutocomplete: function () {
            try {
                // Create PlaceAutocompleteElement options
                let autocompleteOptions = {};
                
                // Map legacy options to new API options
                if (this.GooglePlaceAutocompleteOptions.componentRestrictions && 
                    this.GooglePlaceAutocompleteOptions.componentRestrictions.country) {
                    const countries = Array.isArray(this.GooglePlaceAutocompleteOptions.componentRestrictions.country) 
                        ? this.GooglePlaceAutocompleteOptions.componentRestrictions.country 
                        : [this.GooglePlaceAutocompleteOptions.componentRestrictions.country];
                    autocompleteOptions.includedRegionCodes = countries;
                }

                if (this.GooglePlaceAutocompleteOptions.types) {
                    autocompleteOptions.includedPrimaryTypes = this.GooglePlaceAutocompleteOptions.types;
                }

                // Create the new PlaceAutocompleteElement
                this.placeAutocompleteElement = new google.maps.places.PlaceAutocompleteElement(autocompleteOptions);
                
                // Set placeholder if specified
                const placeholder = this.addressAutoCompleteInput.placeholder || this.addressAutoCompleteInput.getAttribute('placeholder');
                if (placeholder) {
                    this.placeAutocompleteElement.placeholder = placeholder;
                }

                // Replace the input with the new element
                this.addressAutoCompleteInput.style.display = 'none';
                this.addressAutoCompleteInput.parentNode.insertBefore(this.placeAutocompleteElement, this.addressAutoCompleteInput.nextSibling);

                // Set bounds if map is available
                if (this.map) {
                    this.placeAutocompleteElement.locationBias = this.map.getBounds();
                }

                // Add event listener for place selection
                this.placeAutocompleteElement.addEventListener('gmp-select', this.handleNewAutoCompletePlaceChange.bind(this));
                
                // Add keyboard event listener to the new element
                this.placeAutocompleteElement.addEventListener('keydown', this.handleAutoCompleteInputKeyDown.bind(this));

                console.log('New PlaceAutocompleteElement initialized successfully');

            } catch (error) {
                console.warn('Failed to initialize new PlaceAutocompleteElement, falling back to legacy:', error);
                this.initializeLegacyPlaceAutocomplete();
            }
        },

        initializeLegacyPlaceAutocomplete: function () {
            this.autocomplete = new google.maps.places.Autocomplete(this.addressAutoCompleteInput, this.GooglePlaceAutocompleteOptions);
            this.autocomplete.bindTo("bounds", this.map);
            this.autocomplete.addListener("place_changed", this.handleAutoCompletePlaceChange.bind(this, this.autocomplete));
            this.addressAutoCompleteInput.addEventListener('keydown', this.handleAutoCompleteInputKeyDown.bind(this));
        },

        handleNewAutoCompletePlaceChange: async function (event) {
            try {
                const placePrediction = event.placePrediction;
                const place = placePrediction.toPlace();
                
                // Fetch required fields
                await place.fetchFields({
                    fields: ['displayName', 'formattedAddress', 'location', 'geometry']
                });

                // Convert to legacy-compatible format
                const legacyPlace = {
                    geometry: {
                        location: {
                            lat: () => place.location.lat,
                            lng: () => place.location.lng
                        }
                    },
                    formatted_address: place.formattedAddress,
                    name: place.displayName
                };

                const lat = place.location.lat;
                const lng = place.location.lng;
                this.addMarkerToMap(lat, lng);
                this.updateDjangoInput(legacyPlace);
                this.fitBoundMarker();

                // Update the hidden input field to show selected address
                if (this.addressAutoCompleteInput) {
                    this.addressAutoCompleteInput.value = place.formattedAddress || '';
                }

            } catch (error) {
                console.error('Error handling new autocomplete place selection:', error);
            }
        },

        // Clear autocomplete - supports both APIs
        clearAutocomplete: function() {
            if (this.placeAutocompleteElement) {
                // For new API, we need to clear the element
                this.placeAutocompleteElement.value = '';
            }
            if (this.addressAutoCompleteInput) {
                this.addressAutoCompleteInput.value = '';
            }
        },

        // Update bounds for autocomplete - supports both APIs
        updateAutocompleteBounds: function() {
            if (this.map) {
                const bounds = this.map.getBounds();
                if (this.placeAutocompleteElement && bounds) {
                    this.placeAutocompleteElement.locationBias = bounds;
                }
                if (this.autocomplete && bounds) {
                    this.autocomplete.setBounds(bounds);
                }
            }
        },

        addMarkerToMap: function (lat, lng) {
            this.removeMarker();
            const marker_position = {lat: parseFloat(lat), lng: parseFloat(lng)};
            this.marker = new google.maps.marker.AdvancedMarkerElement({
                map: this.map,
                position: marker_position,
                gmpDraggable: true
            });
            this.marker.addListener("dragend", this.dragMarker.bind(this));
        },

        serializeMarkerToGeoJSON: function () {
            if (this.marker) {
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
            if (this.markerFitZoom && this.isInt(this.markerFitZoom)) {
                const markerFitZoom = parseInt(this.markerFitZoom);
                const listener = google.maps.event.addListener(this.map, "idle", function () {
                    if (this.getZoom() > markerFitZoom) {
                        this.setZoom(markerFitZoom)
                    }
                    google.maps.event.removeListener(listener);
                });
            }
        },

        removeMarker: function (e) {
            if (this.marker) {
                this.marker.setMap(null);
            }
            this.marker = null;
        },

        dragMarker: function (e) {
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
            if (keyCode === 13) {  // pressed enter key
                e.preventDefault();
                return false;
            }
        },

        handleAddMarkerBtnClick: function (e) {
            $(this.mapElement).toggleClass("click");
            this.addMarkerBtn.toggleClass("active");
            if ($(this.addMarkerBtn).hasClass("active")) {
                this.map.addListener("click", this.handleMapClick.bind(this));
            } else {
                google.maps.event.clearListeners(this.map, 'click');
            }
        },

        handleMapClick: function (e) {
            google.maps.event.clearListeners(this.map, 'click');
            $(this.mapElement).removeClass("click");
            this.addMarkerBtn.removeClass("active");
            this.addMarkerToMap(e.latLng.lat(), e.latLng.lng())
            this.updateDjangoInput()
        },

        callPlaceTriggerHandler: function (lat, lng, place) {
            if (place === undefined) {
                var latlng = {lat: parseFloat(lat), lng: parseFloat(lng)};
                this.geocoder.geocode({'location': latlng}, function (results, status) {
                    if (status === google.maps.GeocoderStatus.OK) {
                        var placeObj = results[0] || {};
                        $(this.addressAutoCompleteInput).val(placeObj.formatted_address || "");
                        $(document).trigger(this.placeChangedTriggerNameSpace,
                            [placeObj, lat, lng, this.wrapElemSelector, this.djangoInput]
                        );
                        if ($.isEmptyObject(this.djangoGeoJSONValue)) {
                            $(document).trigger(this.markerCreateTriggerNameSpace,
                                [placeObj, lat, lng, this.wrapElemSelector, this.djangoInput]
                            );
                        } else {
                            $(document).trigger(this.markerChangeTriggerNameSpace,
                                [placeObj, lat, lng, this.wrapElemSelector, this.djangoInput]
                            );
                        }
                    }
                }.bind(this));
            } else {  // user entered an address
                $(document).trigger(this.placeChangedTriggerNameSpace,
                    [place, lat, lng, this.wrapElemSelector, this.djangoInput]
                );
            }
        },
    });

})(mapWidgets.jQuery);
