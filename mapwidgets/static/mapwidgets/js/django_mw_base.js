$.namespace("DjangoMapWidgetBase");


DjangoMapWidgetBase = $.Class.extend({

    init: function(options){
        $.extend(this, options);
        this.coordinatesOverlayToggleBtn.on("click", this.toggleCoordinatesOverlay.bind(this));
        this.coordinatesOverlayDoneBtn.on("click", this.handleCoordinatesOverlayDoneBtnClick.bind(this));
        this.coordinatesOverlayInputs.on("change", this.handleCoordinatesInputsChange.bind(this));
        this.resetBtn.on("click", this.resetMap.bind(this));
        this.addMarkerBtn.on("click", this.handleAddMarkerBtnClick.bind(this));
        this.myLocationBtn.on("click", this.handleMyLocationBtnClick.bind(this));

        var autocomplete = new google.maps.places.Autocomplete(this.addressAutoCompleteInput);
        google.maps.event.addListener(autocomplete, 'place_changed', function() {
            var place = autocomplete.getPlace();
            var lat = place.geometry.location.lat();
            var lng = place.geometry.location.lng();
            this.updateLocationInput(lat, lng);
        }.bind(this));

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
        this.hideOverlay();
    },

    toggleCoordinatesOverlay: function(){
        this.coordinatesOverlayToggleBtn.toggleClass("active");
        $("#mw-coordinates-overlay").toggleClass("hide");
    },

    updateCoordinatesInputs: function(lat, lng){
        $("#mw-overlay-latitude").val(lat || "");
        $("#mw-overlay-longitude").val(lng || "");
    },

    handleCoordinatesInputsChange: function (e) {
        var lat = $("#mw-overlay-latitude").val()
        var lng = $("#mw-overlay-longitude").val()
    },

    handleCoordinatesOverlayDoneBtnClick: function(){
        $("input", ".mw-coordinates-overlay").removeClass("error");
        var lat_input = $("#mw-overlay-latitude");
        var lng_input = $("#mw-overlay-longitude");
        var lat = lat_input.val();
        var lng = lng_input.val();
        if (lat && lng){
            this.updateLocationInput(lat, lng);
        }
        $("#mw-coordinates-overlay").addClass("hide");
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
        this.updateLocationInput(location.coords.latitude, location.coords.longitude)
    },

    handlecurrentPositionError: function(){
        this.hideOverlay();
        alert("Your location could not be found.");
    },

    resetMap: function(){
        this.hideOverlay();
        this.locationInput.val("");
        this.removeMarker()
    },

    showOverlay: function(){
        this.loaderOverlayElem.removeClass("hide")
    },

    hideOverlay: function(){
        this.loaderOverlayElem.addClass("hide")
    }
});