from mapwidgets.settings import mw_settings
from mapwidgets.widgets.base import BasePointFieldWidget


class MapboxPointFieldWidget(BasePointFieldWidget):
    template_name = "mapwidgets/pointfield/mapbox/interactive_widget.html"
    settings = mw_settings.Mapbox.PointField.interactive
    settings_namespace = "mw_settings.Mapbox.PointField.interactive"

    @property
    def media(self):
        return self.generate_media(
            js_sources=[
                "https://api.mapbox.com/mapbox-gl-js/v2.5.1/mapbox-gl.js",
                "https://unpkg.com/@mapbox/mapbox-sdk/umd/mapbox-sdk.min.js",
                "https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.7.2/mapbox-gl-geocoder.min.js",
            ],
            css_files=[
                "mapwidgets/css/map_widgets{}.css",
                "https://api.mapbox.com/mapbox-gl-js/v2.5.1/mapbox-gl.css",
                "https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.7.2/mapbox-gl-geocoder.css",
            ],
            min_js="mapwidgets/js/pointfield/interactive/mapbox/mw_pointfield.min.js",
            dev_js=[
                "mapwidgets/js/mw_init.js",
                "mapwidgets/js/mw_jquery_class.js",
                "mapwidgets/js/pointfield/interactive/mw_pointfield_base.js",
                "mapwidgets/js/pointfield/interactive/mapbox/mw_pointfield.js",
            ],
        )
