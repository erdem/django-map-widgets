(function($) {
	DjangoMapWidgetBase = $.Class.extend({

		init: function(options){
			$.extend(this, options);
			this.coordinatesOverlayToggleBtn.on("click", this.toggleCoordinatesOverlay.bind(this));
			this.coordinatesOverlayDoneBtn.on("click", this.handleCoordinatesOverlayDoneBtnClick.bind(this));
			this.coordinatesOverlayInputs.on("change", this.handleCoordinatesInputsChange.bind(this));
			this.addMarkerBtn.on("click", this.handleAddMarkerBtnClick.bind(this));
			this.myLocationBtn.on("click", this.handleMyLocationBtnClick.bind(this));
			this.deleteBtn.on("click", this.resetMap.bind(this));

			// if the location field in a collapse on Django admin form, the map need to initialize again when the collapse open by user.
			if ($(this.wrapElemSelector).closest('.module.collapse').length){
				$(document).on('show.fieldset', this.initializeMap.bind(this));
			}
			this.initializeMap.bind(this)();
		},

		initializeMap: function(){
			console.warn("Implement initializeMap method.");
		},

		updateMap: function(lat, lng){
			console.warn("Implement updateMap method.");
		},

		addMarkerToMap: function(lat, lng){
			console.warn("Implement this method for your map js library.");
		},

		fitBoundMarker: function(){
			console.warn("Implement this method for your map js library.");
		},

		removeMarker: function(){
			console.warn("Implement this method for your map js library.");
		},

		dragMarker: function(e){
			console.warn("Implement dragMarker method.");
		},

		handleMapClick: function(e){
			console.warn("Implement handleMapClick method.");
		},

		handleAddMarkerBtnClick: function(e){
			console.warn("Implement handleAddMarkerBtnClick method.");
		},

		isInt : function(value) {
			return !isNaN(value) &&
				parseInt(Number(value)) === value &&
				!isNaN(parseInt(value, 10));
		},

		serializeMarkerToGeoJSON: function(){
			console.warn("Implement serializeMarkerToGeoJSON method.");
		},

		callPlaceTriggerHandler: function (lat, lng, place) {
			if (place === undefined){
                var latlng = {lat: parseFloat(lat), lng: parseFloat(lng)};
				this.geocoder.geocode({'location' : latlng}, function(results, status) {
                    if (status === google.maps.GeocoderStatus.OK) {
	                    var placeObj = results[0] || {};
	                    $(this.addressAutoCompleteInput).val(placeObj.formatted_address || "");
	                    $(document).trigger(this.placeChangedTriggerNameSpace,
		                    [placeObj, lat, lng, this.wrapElemSelector, this.djangoInput]
	                    );
						if ($.isEmptyObject(this.djangoGeoJSONValue)){
							$(document).trigger(this.markerCreateTriggerNameSpace,
								[placeObj, lat, lng, this.wrapElemSelector, this.djangoInput]
							);
						}else{
							$(document).trigger(this.markerChangeTriggerNameSpace,
								[placeObj, lat, lng, this.wrapElemSelector, this.djangoInput]
							);
						}
                    }
                }.bind(this));
			}else{  // user entered an address
				$(document).trigger(this.placeChangedTriggerNameSpace,
					[place, lat, lng, this.wrapElemSelector, this.djangoInput]
				);
			}
		},

		updateDjangoGeoJSONValue: function(lat, lng){
			if (this.djangoGeoJSONValue){
				this.djangoGeoJSONValue.lat = lat;
				this.djangoGeoJSONValue.lng = lng;
			}else{
				this.djangoGeoJSONValue = {
					"lng": lng,
					"lat": lat
				};
			}
		},

		enableClearBtn: function(){
			this.deleteBtn.removeClass("mw-btn-default disabled").addClass("mw-btn-danger");
		},

		disableClearBtn: function(){
			this.deleteBtn.removeClass("mw-btn-danger").addClass("mw-btn-default disabled");
		},

		updateDjangoInput: function(place){
			const django_input_val = this.serializeMarkerToGeoJSON();
			const lng = django_input_val.coordinates[0];
			const lat = django_input_val.coordinates[1];
			this.djangoInput.val(JSON.stringify(django_input_val));
			this.updateUXCoordinatesInputs(lat, lng);
			this.callPlaceTriggerHandler(lat, lng, place);
			this.updateDjangoGeoJSONValue(lat, lng);
			this.enableClearBtn();
		},

		resetMap: function(){
			if (!$.isEmptyObject(this.djangoGeoJSONValue)) {
				this.hideOverlay();
				this.djangoInput.val("");
				this.coordinatesOverlayInputs.val("");
				$(this.addressAutoCompleteInput).val("");
				this.addMarkerBtn.removeClass("active");
				this.removeMarker();
				this.disableClearBtn();
				$(document).trigger(this.markerDeleteTriggerNameSpace,
					[
						this.djangoGeoJSONValue.lat,
						this.djangoGeoJSONValue.lng,
						this.wrapElemSelector,
						this.djangoInput
					]
				);
				this.djangoGeoJSONValue = null;
			}
		},

		toggleCoordinatesOverlay: function(){
			this.coordinatesOverlayToggleBtn.toggleClass("active");
			$(".mw-coordinates-overlay", this.wrapElemSelector).toggleClass("hide");
		},

		updateUXCoordinatesInputs: function(lat, lng){
			$(".mw-overlay-latitude", this.wrapElemSelector).val(lat || "");
			$(".mw-overlay-longitude", this.wrapElemSelector).val(lng || "");
		},

		handleCoordinatesInputsChange: function (e) {
			var lat = $(".mw-overlay-latitude", this.wrapElemSelector).val();
			var lng = $(".mw-overlay-longitude", this.wrapElemSelector).val();
			if (lat && lng){
				this.addMarkerToMap(lat, lng);
				this.updateDjangoInput();
				this.fitBoundMarker();
			}
		},

		handleCoordinatesOverlayDoneBtnClick: function(){
			$(".mw-coordinates-overlay", this.wrapElemSelector).addClass("hide");
			this.coordinatesOverlayToggleBtn.removeClass("active");
		},

		handleMyLocationBtnClick: function(){
			this.showOverlay();
			if(navigator.geolocation){
				navigator.geolocation.getCurrentPosition(
					this.handleCurrentPosition.bind(this),
					this.handlecurrentPositionError.bind(this)
				);
			}else{
				this.handlecurrentPositionError();
			}

		},

		handleCurrentPosition: function(location){
			this.addMarkerToMap(location.coords.latitude, location.coords.longitude);
			this.updateDjangoInput();
			this.hideOverlay();
			this.fitBoundMarker();
		},

		handlecurrentPositionError: function(){
			this.hideOverlay();
			alert("Your location could not be found.");
		},

		showOverlay: function(){
			this.loaderOverlayElem.removeClass("hide")
		},

		hideOverlay: function(){
			this.loaderOverlayElem.addClass("hide")
		}
	});

})(mapWidgets.jQuery);
