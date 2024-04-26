from django import forms
from django.contrib.gis.geos import Point
from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static
from django.utils.http import urlencode

from mapwidgets.constants import STATIC_MAP_PLACEHOLDER_IMAGE
from mapwidgets.settings import mw_settings
from mapwidgets.utils import AsyncJS, minify_if_not_debug
from mapwidgets.widgets.base import BasePointFieldWidget, BasePointFieldStaticWidget
from mapwidgets.widgets.mixins import PointFieldInlineWidgetMixin


class GoogleMapPointFieldWidget(BasePointFieldWidget):
    template_name = 'mapwidgets/googlemap/pointfield/interactive_widget.html'
    settings = mw_settings.GoogleMap.PointField.interactive
    settings_namespace = 'mw_settings.GoogleMap.PointField.interactive'

    @property
    def _google_map_js_url(self):
        if mw_settings.GoogleMap.apiKey is None:
            raise ImproperlyConfigured("`GoogleMap.apiKey` setting is required to use Google Map widgets.")
        cdn_url_params = {
            "key": mw_settings.GoogleMap.apiKey,
            "callback": "googleMapWidgetsCallback"
        }
        cdn_url_params.update(mw_settings.GoogleMap.dict()["CDNURLParams"])
        return f"https://maps.googleapis.com/maps/api/js?{urlencode(cdn_url_params)}"

    @property
    def media(self):
        return self.generate_media(
            js_sources=[
                AsyncJS(self._google_map_js_url)
            ],
            css_files=[
                'mapwidgets/css/map_widgets{}.css',
            ],
            min_js='mapwidgets/js/mw_google_point_field.min.js',
            dev_js=[
                'mapwidgets/js/mw_init.js',
                'mapwidgets/js/mw_jquery_class.js',
                'mapwidgets/js/mw_pointfield_base.js',
                'mapwidgets/js/mw_google_point_field.js'
            ]
        )


class GoogleMapPointFieldInlineWidget(PointFieldInlineWidgetMixin, GoogleMapPointFieldWidget):
    template_name = 'mapwidgets/googlemap/pointfield/interactive_inline_widget.html'
    settings = mw_settings.GoogleMap.PointField.interactive
    settings_namespace = 'mw_settings.GoogleMap.PointField.interactive'

    @property
    def media(self):
        js = [AsyncJS(self._google_map_js_url)]

        css = {
            'all': [
                minify_if_not_debug('mapwidgets/css/map_widgets{}.css'),
            ]
        }

        if not mw_settings.MINIFED:  # pragma: no cover
            js = js + [
                'mapwidgets/js/mw_init.js',
                'mapwidgets/js/mw_jquery_class.js',
                'mapwidgets/js/mw_pointfield_base.js',
                'mapwidgets/js/mw_google_point_field.js',
                'mapwidgets/js/mw_google_point_field_generater.js'
            ]
        else:
            js = js + [
                'mapwidgets/js/mw_google_point_inline_field.min.js'
            ]

        return forms.Media(js=js, css=css)


class GoogleMapPointFieldStaticWidget(BasePointFieldStaticWidget):
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    settings = mw_settings.GoogleMap.PointField
    template_name = "mapwidgets/googlemap/pointfield/static_widget.html"

    def __init__(self, zoom=None, size=None, *args, **kwargs):
        self.zoom = zoom
        self.size = size
        super(GoogleMapPointFieldStaticWidget, self).__init__(*args, **kwargs)

    @property
    def map_settings(self):
        self.settings["key"] = mw_settings.GOOGLE_MAP_API_KEY

        if mw_settings.GOOGLE_MAP_API_SIGNATURE:  # pragma: no cover
            self.settings["signature"] = mw_settings.GOOGLE_MAP_API_SIGNATURE

        if self.size:
            self.settings["size"] = self.size
            self.settings["zoom"] = self.zoom
        return self.settings

    @property
    def marker_settings(self):
        if not isinstance(mw_settings.GoogleStaticMapMarkerSettings, dict):  # pragma: no cover
            raise TypeError('GoogleStaticMapMarkerSettings must be a dictionary.')

        return mw_settings.GoogleStaticMapMarkerSettings

    def get_point_field_params(self, latitude, longitude):
        marker_point = "%s,%s" % (latitude, longitude)

        marker_params = ["%s:%s" % (key, value) for key, value in self.marker_settings.items()]
        marker_params.append(marker_point)
        marker_url_params = "|".join(marker_params)
        params = {
            "center": marker_point,
            "markers": marker_url_params,
        }
        params.update(self.map_settings)
        return params

    def get_image_url(self, value):
        if isinstance(value, Point):
            longitude, latitude = value.x, value.y
            params = self.get_point_field_params(latitude, longitude)

            image_url_template = "%(base_url)s?%(params)s"
            image_url_data = {
                "base_url": self.base_url,
                "params": urlencode(params)
            }
            return image_url_template % image_url_data

        return static(STATIC_MAP_PLACEHOLDER_IMAGE)


class GoogleMapPointFieldStaticOverlayWidget(GoogleMapPointFieldStaticWidget):
    settings = mw_settings.GoogleMap.PointField
    template_name = "mapwidgets/googlemap/pointfield/static_overlay_widget.html"

    class Media:
        css = {
            "all": (
                minify_if_not_debug("mapwidgets/css/magnific-popup{}.css"),
            )
        }
        if not mw_settings.MINIFED:  # pragma: no cover
            js = (
                "mapwidgets/js/mw_init.js",
                "mapwidgets/js/jquery.custom.magnific-popup.js",
            )
        else:
            js = (
                "mapwidgets/js/jquery.custom.magnific-popup.min.js",
            )

    def __init__(self, zoom=None, size=None, thumbnail_size=None, *args, **kwargs):
        self.thumbnail_size = thumbnail_size
        super(GoogleMapPointFieldStaticOverlayWidget, self).__init__(zoom, size, *args, **kwargs)

    @property
    def map_settings(self):
        settings = super(GoogleMapPointFieldStaticOverlayWidget, self).map_settings
        if self.thumbnail_size:
            settings["thumbnail_size"] = self.thumbnail_size
        return settings

    def get_thumbnail_url(self, value):
        if isinstance(value, Point):
            longitude, latitude = value.x, value.y
            params = self.get_point_field_params(latitude, longitude)
            params["size"] = params["thumbnail_size"]
            image_url_template = "%(base_url)s?%(params)s"
            image_url_data = {
                "base_url": self.base_url,
                "params": urlencode(params)
            }
            return image_url_template % image_url_data
        return static(STATIC_MAP_PLACEHOLDER_IMAGE)

    def get_context_data(self, name, value, attrs):
        context = super(GoogleMapPointFieldStaticOverlayWidget, self).get_context_data(name, value, attrs)
        context["thumbnail_url"] = self.get_thumbnail_url(value)
        return context
