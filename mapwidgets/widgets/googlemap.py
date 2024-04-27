from django import forms
from django.contrib.gis.geos import Point
from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static
from django.utils.http import urlencode

from mapwidgets.constants import STATIC_MAP_PLACEHOLDER_IMAGE
from mapwidgets.settings import mw_settings
from mapwidgets.utils import AsyncJS
from mapwidgets.widgets.base import BasePointFieldWidget, BasePointFieldStaticWidget
from mapwidgets.widgets.mixins import PointFieldInlineWidgetMixin


class GoogleMapPointFieldWidget(BasePointFieldWidget):
    template_name = "mapwidgets/pointfield/googlemap/interactive_widget.html"
    settings = mw_settings.GoogleMap.PointField.interactive
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
        cdn_url_params.update(mw_settings.GoogleMap.dict()["CDNURLParams"])
        return f"https://maps.googleapis.com/maps/api/js?{urlencode(cdn_url_params)}"

    @property
    def media(self):
        return self.generate_media(
            js_sources=[AsyncJS(self._google_map_js_url)],
            css_files=[
                "mapwidgets/css/map_widgets.css",
            ],
            min_js="mapwidgets/js/pointfield/interactive/googlemap/mw_pointfield.min.js",
            dev_js=[
                "mapwidgets/js/mw_init.js",
                "mapwidgets/js/mw_jquery_class.js",
                "mapwidgets/js/pointfield/interactive/mw_pointfield_base.js",
                "mapwidgets/js/pointfield/interactive/googlemap/mw_pointfield.js",
            ],
        )


class GoogleMapPointFieldInlineWidget(
    PointFieldInlineWidgetMixin, GoogleMapPointFieldWidget
):
    template_name = "mapwidgets/pointfield/googlemap/interactive_inline_widget.html"
    settings = mw_settings.GoogleMap.PointField.interactive
    settings_namespace = "mw_settings.GoogleMap.PointField.interactive"

    @property
    def media(self):
        js = [AsyncJS(self._google_map_js_url)]

        css = {
            "all": [
                "mapwidgets/css/map_widgets.css",
            ]
        }

        if not mw_settings.MINIFED:  # pragma: no cover
            js = js + [
                "mapwidgets/js/mw_init.js",
                "mapwidgets/js/mw_jquery_class.js",
                "mapwidgets/js/pointfield/interactive/mw_pointfield_base.js",
                "mapwidgets/js/pointfield/interactive/googlemap/mw_pointfield.js",
                "mapwidgets/js/pointfield/interactive/googlemap/mw_pointfield_inline_generater.js",
            ]
        else:
            js = js + [
                "mapwidgets/js/pointfield/interactive/googlemap/mw_pointfield_inline.min.js"
            ]

        return forms.Media(js=js, css=css)
