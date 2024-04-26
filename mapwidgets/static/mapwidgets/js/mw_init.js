let mapWidgets = {};

// Array to store callback functions for Google Maps widget Classes
// These functions will be executed when the Google Maps API finishes loading
mapWidgets.googleMapCallbacks = []

// First, try to use the jQuery instance from Django Admin (if available)
// If Django Admin jQuery is not available, use the global jQuery instance
if (typeof django !== "undefined" && django.jQuery){
    mapWidgets.jQuery = django.jQuery.noConflict();
}else{
    mapWidgets.jQuery = jQuery.noConflict();
}


// This callback function execute by GoogleMap JS.
function googleMapWidgetsCallback(){
    window.addEventListener("load", (event) => {
        for (let index = 0; index < mapWidgets.googleMapCallbacks.length; index++) {
            const widgetCallback = mapWidgets.googleMapCallbacks[index]
            new widgetCallback.class(widgetCallback.options)
        }
    });
}
