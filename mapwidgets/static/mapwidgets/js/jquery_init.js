var mapWidgets = mapWidgets || {};

// Use Django Admin jQuery function if exists, otherwise initialise `mapWidgets.jQuery` from global jQuery.
if (typeof django !== "undefined" && django.jQuery){
    mapWidgets.jQuery = django.jQuery.noConflict();
}else{
    mapWidgets.jQuery = jQuery.noConflict();
}