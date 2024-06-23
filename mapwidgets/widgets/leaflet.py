from django.forms import Media

from mapwidgets.settings import mw_settings
from mapwidgets.widgets.base import BasePointFieldInteractiveWidget


class LeafletPointFieldWidget(BasePointFieldInteractiveWidget):
    template_name = "mapwidgets/pointfield/leaflet/interactive.html"
    _settings = mw_settings.Leaflet.PointField.interactive

    @property
    def media(self):
        return self._media(
            extra_css=[
                "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
            ],
            extra_js=[
                "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
            ],
        )
