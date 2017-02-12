(function($) {
    DjangoMapWidgetBase = $.Class.extend({

        init: function(options){
            $.extend(this, options);
            this.coordinatesOverlayToggleBtn.on("click", this.toggleCoordinatesOverlay.bind(this));
            this.coordinatesOverlayDoneBtn.on("click", this.handleCoordinatesOverlayDoneBtnClick.bind(this));
            this.coordinatesOverlayInputs.on("change", this.handleCoordinatesInputsChange.bind(this));
            this.addMarkerBtn.on("click", this.handleAddMarkerBtnClick.bind(this));
            this.myLocationBtn.on("click", this.handleMyLocationBtnClick.bind(this));
            this.deleteBtn.on("click", this.deleteMarker.bind(this));
            var autocomplete = new google.maps.places.Autocomplete(this.addressAutoCompleteInput, this.GooglePlaceAutocompleteOptions);
            google.maps.event.addListener(autocomplete, 'place_changed', this.handleAutoCompletePlaceChange.bind(this, autocomplete));
            google.maps.event.addDomListener(this.addressAutoCompleteInput, 'keydown', this.handleAutoCompleteInputKeyDown.bind(this));
            this.initializeMap();
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
                parseInt(Number(value)) == value &&
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

        updateLocationInput: function(lat, lng){
            this.showOverlay();
            var location_input_val = "POINT (" + lng + " " + lat + ")";
            this.locationInput.val(location_input_val);
            this.updateCoordinatesInputs(lat, lng);
            this.addMarkerToMap(lat, lng);
            if ($.isEmptyObject(this.locationFieldValue)){
                $(document).trigger(this.markerCreateTriggerNameSpace,
                    [lat, lng, this.wrapElemSelector, this.locationInput]
                );
            }else{
                $(document).trigger(this.markerChangeTriggerNameSpace,
                    [lat, lng, this.wrapElemSelector, this.locationInput]
                );
            }

            this.locationFieldValue = {
                "lng": lng,
                "lat": lat
            };
            this.deleteBtn.removeClass("btn-default disabled").addClass("btn-danger");
            this.hideOverlay();
        },

        deleteMarker: function(){
            if (!$.isEmptyObject(this.locationFieldValue)) {
                console.log(this.locationFieldValue);
                this.hideOverlay();
                this.locationInput.val("");
                this.coordinatesOverlayInputs.val("");
                this.removeMarker();
                this.deleteBtn.removeClass("btn-danger").addClass("btn-default disabled");
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
            this.fitBoundMarker();
        },

        handlecurrentPositionError: function(){
            this.hideOverlay();
            alert("Your location could not be found.");
        },

        handleAutoCompleteInputKeyDown: function (e) {
            if (e.keyCode == 13){  // pressed enter key
                e.preventDefault();
            }
        },

        handleAutoCompletePlaceChange: function (autocomplete) {
            var place = autocomplete.getPlace();
            var lat = place.geometry.location.lat();
            var lng = place.geometry.location.lng();
            this.updateLocationInput(lat, lng);
            this.fitBoundMarker()
        },


        showOverlay: function(){
            this.loaderOverlayElem.removeClass("hide")
        },

        hideOverlay: function(){
            this.loaderOverlayElem.addClass("hide")
        }
    });

})(jQuery || django.jQuery);