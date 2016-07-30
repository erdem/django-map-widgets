(function($) {
    $(document).ready(function() {
        $('.map-widget-overlay-link').magnificPopup({
          type: 'image',
          closeOnContentClick: true,
          closeBtnInside: false,
          fixedContentPos: true,
          mainClass: 'mfp-no-margins mfp-with-zoom',
          image: {
            verticalFit: true
          },
          zoom: {
            enabled: true,
            duration: 300
          }
        });
    });
})(jQuery || django.jQuery);