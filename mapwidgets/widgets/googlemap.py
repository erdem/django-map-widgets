from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.utils.http import urlencode

from mapwidgets.settings import mw_settings
from mapwidgets.utils import AsyncJS
from mapwidgets.widgets.base import BasePointFieldWidget
from mapwidgets.widgets.mixins import PointFieldInlineWidgetMixin


class GoogleMapPointFieldWidget(BasePointFieldWidget):
    template_name = "mapwidgets/pointfield/googlemap/interactive_widget.html"
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
    template_name = "mapwidgets/pointfield/googlemap/interactive_inline_widget.html"
    _settings = mw_settings.GoogleMap.PointField.interactive
    settings_namespace = "mw_settings.GoogleMap.PointField.interactive"

    def dev_media(self, extra_css=None, extra_js=None):
        """
        Append inline generator js to `GoogleMapPointFieldWidget` dev JS files.
        """
        settings = super().dev_media(extra_css, extra_js)
        inline_generator_js = "mapwidgets/js/pointfield/interactive/googlemap/mw_pointfield_inline_generator.js"
        settings["js"].append(inline_generator_js)
        return settings

    def minified_media(self, extra_css=None, extra_js=None):
        """
        Provide different new minified file path for Admin Inline Widget
        """
        settings = super().minified_media(extra_css, extra_js)
        settings["js"] = [
            AsyncJS(self._google_map_js_url),
            "mapwidgets/js/pointfield/interactive/googlemap/mw_pointfield_inline.min.js",
        ]
        return settings
