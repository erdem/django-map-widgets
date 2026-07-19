from django.forms import Media

from mapwidgets.settings import mw_settings
from mapwidgets.widgets.base import (
    BasePointFieldInteractiveWidget,
    BasePolygonFieldInteractiveWidget,
)

LEAFLET_CSS = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
LEAFLET_JS = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
LEAFLET_GEOSEARCH_JS = "https://unpkg.com/leaflet-geosearch@4.4.0/dist/geosearch.umd.js"
LEAFLET_GEOCODER_JS = (
    "https://unpkg.com/leaflet-control-geocoder@3.3.1/dist/Control.Geocoder.js"
)


class LeafletPointFieldWidget(BasePointFieldInteractiveWidget):
    template_name = "mapwidgets/pointfield/leaflet/interactive.html"
    _settings = mw_settings.Leaflet.PointField.interactive

    @property
    def media(self):
        extra_js = [LEAFLET_JS]
        geo_search = self.settings.geoSearch
        if geo_search and geo_search.enabled:
            extra_js.append(LEAFLET_GEOSEARCH_JS)
            # leaflet-control-geocoder is only used to reverse geocode the marker
            # location and populate the search bar.
            if geo_search.reverseGeocode:
                extra_js.append(LEAFLET_GEOCODER_JS)
        return self._media(extra_css=[LEAFLET_CSS], extra_js=extra_js)


class LeafletPolygonFieldWidget(BasePolygonFieldInteractiveWidget):
    template_name = "mapwidgets/polygonfield/leaflet/interactive.html"
    _settings = mw_settings.Leaflet.PolygonField.interactive

    @property
    def media(self):
        extra_js = [LEAFLET_JS]
        if self.settings.geoSearch and self.settings.geoSearch.enabled:
            extra_js.append(LEAFLET_GEOSEARCH_JS)
        return self._media(extra_css=[LEAFLET_CSS], extra_js=extra_js)
