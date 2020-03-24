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
			
			// if the the location field in a collapse on Django admin form, the map need to initialize again when the collapse open by user.
			if ($(this.wrapElemSelector).closest('.module.collapse').length){
				$(document).on('show.fieldset', this.initializeMap.bind(this));
			}
			
			var autocomplete = new google.maps.places.Autocomplete(this.addressAutoCompleteInput, this.GooglePlaceAutocompleteOptions);
			google.maps.event.addListener(autocomplete, 'place_changed', this.handleAutoCompletePlaceChange.bind(this, autocomplete));
			google.maps.event.addDomListener(this.addressAutoCompleteInput, 'keydown', this.handleAutoCompleteInputKeyDown.bind(this));
			this.geocoder = new google.maps.Geocoder;
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
		
		getLocationValues: function(){
			var latlng = this.locationInput.val().split(' ');
			var lat = latlng[2].replace(/[\(\)]/g, '');
			var lng = latlng[1].replace(/[\(\)]/g, '');
			return {
				"lat": lat,
				"lng": lng
			}
		},
		
		callPlaceTriggerHandler: function (lat, lng, place) {
			if (place === undefined){
                var latlng = {lat: parseFloat(lat), lng: parseFloat(lng)};
				this.geocoder.geocode({'location' : latlng}, function(results, status) {
                    if (status === google.maps.GeocoderStatus.OK) {
	                    var placeObj = results[0] || {};
	                    $(this.addressAutoCompleteInput).val(placeObj.formatted_address || "");
	                    $(document).trigger(this.placeChangedTriggerNameSpace,
		                    [placeObj, lat, lng, this.wrapElemSelector, this.locationInput]
	                    );
                    }
                }.bind(this));
			}else{  // user entered an address
				$(document).trigger(this.placeChangedTriggerNameSpace,
					[place, lat, lng, this.wrapElemSelector, this.locationInput]
				);
			}
		},
		
		updateLocationInput: function(lat, lng, place){
			var location_input_val = "POINT (" + lng + " " + lat + ")";
			this.locationInput.val(location_input_val);
			this.updateCoordinatesInputs(lat, lng);
			this.addMarkerToMap(lat, lng);
			if ($.isEmptyObject(this.locationFieldValue)){
				$(document).trigger(this.markerCreateTriggerNameSpace,
					[place, lat, lng, this.wrapElemSelector, this.locationInput]
				);
			}else{
				$(document).trigger(this.markerChangeTriggerNameSpace,
					[place, lat, lng, this.wrapElemSelector, this.locationInput]
				);
			}
			
			this.callPlaceTriggerHandler(lat, lng, place);
			this.locationFieldValue = {
				"lng": lng,
				"lat": lat
			};
			this.deleteBtn.removeClass("mw-btn-default disabled").addClass("mw-btn-danger");
		},
		
		resetMap: function(){
			if (!$.isEmptyObject(this.locationFieldValue)) {
				this.hideOverlay();
				this.locationInput.val("");
				this.coordinatesOverlayInputs.val("");
				$(this.addressAutoCompleteInput).val("");
				this.addMarkerBtn.removeClass("active");
				this.removeMarker();
				this.deleteBtn.removeClass("mw-btn-danger").addClass("mw-btn-default disabled");
				$(document).trigger(this.markerDeleteTriggerNameSpace,
					[
						this.locationFieldValue.lat,
						this.locationFieldValue.lng,
						this.wrapElemSelector,
						this.locationInput
					]
				);
				this.locationFieldValue = null;
			}
		},
		
		toggleCoordinatesOverlay: function(){
			this.coordinatesOverlayToggleBtn.toggleClass("active");
			$(".mw-coordinates-overlay", this.wrapElemSelector).toggleClass("hide");
		},
		
		updateCoordinatesInputs: function(lat, lng){
			$(".mw-overlay-latitude", this.wrapElemSelector).val(lat || "");
			$(".mw-overlay-longitude", this.wrapElemSelector).val(lng || "");
		},
		
		handleCoordinatesInputsChange: function (e) {
			var lat = $(".mw-overlay-latitude", this.wrapElemSelector).val();
			var lng = $(".mw-overlay-longitude", this.wrapElemSelector).val();
			if (lat && lng){
				this.updateLocationInput(lat, lng);
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
			this.updateLocationInput(location.coords.latitude, location.coords.longitude);
			this.hideOverlay();
			this.fitBoundMarker();
		},
		
		handlecurrentPositionError: function(){
			this.hideOverlay();
			alert("Your location could not be found.");
		},
		
		handleAutoCompleteInputKeyDown: function (e) {
			var keyCode = e.keyCode || e.which;
			if (keyCode === 13){  // pressed enter key
				e.preventDefault();
				return false;
			}
		},
		
		handleAutoCompletePlaceChange: function (autocomplete) {
			var place = autocomplete.getPlace();
			var lat = place.geometry.location.lat();
			var lng = place.geometry.location.lng();
			this.updateLocationInput(lat, lng, place);
			this.fitBoundMarker()
		},
		
		
		showOverlay: function(){
			this.loaderOverlayElem.removeClass("hide")
		},
		
		hideOverlay: function(){
			this.loaderOverlayElem.addClass("hide")
		}
	});
	
})(mapWidgets.jQuery);