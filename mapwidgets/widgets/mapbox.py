from mapwidgets.settings import mw_settings
from mapwidgets.widgets.base import BasePointFieldInteractiveWidget


class MapboxPointFieldWidget(BasePointFieldInteractiveWidget):
    template_name = "mapwidgets/pointfield/mapbox/interactive.html"
    _settings = mw_settings.Mapbox.PointField.interactive

    @property
    def settings(self):
        settings = super().settings
        settings["accessToken"] = mw_settings.Mapbox.accessToken
        return settings

    @property
    def media(self):
        return self._media(
            extra_js=[
                "https://api.mapbox.com/mapbox-gl-js/v3.3.0/mapbox-gl.js",
                "https://unpkg.com/@mapbox/mapbox-sdk/umd/mapbox-sdk.min.js",
                "https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.7.2/mapbox-gl-geocoder.min.js",
            ],
            extra_css=[
                "https://api.mapbox.com/mapbox-gl-js/v3.3.0/mapbox-gl.css",
                "https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.7.2/mapbox-gl-geocoder.css",
            ],
        )
