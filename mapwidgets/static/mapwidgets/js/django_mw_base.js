$.namespace("DjangoMapWidgetBase");


DjangoMapWidgetBase = $.Class.extend({

    init: function(options){
        console.log(options);
        $.extend(this, options);
        this.coordinatesOverlayToggleBtn.on("click", this.toggleCoordinatesOverlay.bind(this));
        this.coordinatesOverlayDoneBtn.on("click", this.handleCoordinatesOverlayDoneBtnClick.bind(this));
        this.resetBtn.on("click", this.resetMap.bind(this));
        this.addMarkerBtn.on("click", this.handleAddMarkerBtnClick.bind(this));
        this.myLocationBtn.on("click", this.handleMyLocationBtnClick.bind(this));

        var geocoder = new google.maps.Geocoder();
        if (this.landingLocationName && geocoder){
            geocoder.geocode({'address' : this.landingLocationName}, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    var location = results[0].geometry.location;
                    this.landingLocation = {
                        lat: location.lat(),
                        lng: location.lng()
                    };
                    this.initializeMap();
                }else{
                    this.initializeMap()
                }
            }.bind(this));
        }else{
            this.initializeMap();
        }
        console.log(this.addressAutoCompleteInput);
        var autocomplete = new google.maps.places.Autocomplete(this.addressAutoCompleteInput);
        google.maps.event.addListener(autocomplete, 'place_changed', function() {
            var place = autocomplete.getPlace();
            var lat = place.geometry.location.lat();
            var lng = place.geometry.location.lng();
            this.updateLocationInput(lat, lng);
        }.bind(this));
    },

    initializeMap: function(){
        console.warn("Implement initializeMap method.");
    },

    addMarkerToMap: function(lat, lng){
        console.warn("Implement this method for your map js library.")
    },

    removeMarker: function(){
        console.warn("Implement this method for your map js library.")
    },

    dragMarker: function(e){
        
    },

    handleMapClick: function(e){

    },

    handleAddMarkerBtnClick: function(e){

    },

    getLocation: function(){
        var latlng = this.locationInput.val().split(' ');
        var lat = latlng[2].replace(/[\(\)]/g, '');
        var lng = latlng[1].replace(/[\(\)]/g, '');
        return {
            "lat": lat,
            "lng": lng
        }
    },

    updateCoordinatesOverlayInputs: function(lat, lng){
        $("#mw-overlay-latitude").val(lat || "");
        $("#mw-overlay-longitude").val(lng || "");
    },

    updateLocationInput: function(lat, lng){
        this.showOverlay();
        var location_input_val = "POINT (" + lng + " " + lat + ")";
        this.locationInput.val(location_input_val);
        this.updateCoordinatesOverlayInputs(lat, lng);
        this.addMarkerToMap(lat, lng);
        this.hideOverlay();
    },

    toggleCoordinatesOverlay: function(){
        this.coordinatesOverlayToggleBtn.toggleClass("active");
        $("#mw-coordinates-overlay").toggleClass("hide");
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
        alert("Your location could not be found.")
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