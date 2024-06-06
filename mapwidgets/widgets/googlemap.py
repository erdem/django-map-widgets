from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.utils.http import urlencode

from mapwidgets.settings import mw_settings
from mapwidgets.utils import AsyncJS
from mapwidgets.widgets.base import BasePointFieldWidget
from mapwidgets.widgets.mixins import PointFieldInlineWidgetMixin


class GoogleMapPointFieldWidget(BasePointFieldWidget):
    template_name = "mapwidgets/pointfield/googlemap/interactive.html"
    _settings = mw_settings.GoogleMap.PointField.interactive
    settings_namespace = "mw_settings.GoogleMap.PointField.interactive"

    @property
    def _google_map_js_url(self):
        if mw_settings.GoogleMap.apiKey is None:
            raise ImproperlyConfigured(
                "`GoogleMap.apiKey` setting is required to use Google Map widgets."
            )
        cdn_url_params = {
            "key": mw_settings.GoogleMap.apiKey,
            "callback": "googleMapWidgetsCallback",
        }
        cdn_url_params.update(mw_settings.GoogleMap["CDNURLParams"])
        return f"https://maps.googleapis.com/maps/api/js?{urlencode(cdn_url_params)}"

    @property
    def media(self):
        return self._media(extra_js=[AsyncJS(self._google_map_js_url)])


class GoogleMapPointFieldInlineWidget(
    PointFieldInlineWidgetMixin, GoogleMapPointFieldWidget
):
    template_name = "mapwidgets/pointfield/googlemap/interactive_inline.html"
    _settings = mw_settings.GoogleMap.PointField.interactive
    settings_namespace = "mw_settings.GoogleMap.PointField.interactive"

    def get_js_paths(self, extra_js=None, minified=False):
        js_paths = super().get_js_paths(extra_js, minified)

        if minified:
            js_paths = [
                AsyncJS(self._google_map_js_url),
                "mapwidgets/js/pointfield/interactive/googlemap/mw_pointfield_inline.min.js",
            ]
        else:
            inline_generator_js = "mapwidgets/js/pointfield/interactive/googlemap/mw_pointfield_inline_generator.js"
            js_paths.append(inline_generator_js)

        return js_paths
