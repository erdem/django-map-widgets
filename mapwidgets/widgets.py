import json

from django import forms
from django.conf import settings
from django.contrib.gis.forms import BaseGeometryWidget
from django.contrib.gis.geos import Point
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils import six
from django.utils.html import format_html
from django.utils.http import urlencode

from mapwidgets.constants import STATIC_MAP_PLACEHOLDER_IMAGE
from mapwidgets.settings import mw_settings


def minify_if_not_debug(asset):
    """
        Transform template string `asset` by inserting '.min' if DEBUG=False
    """
    return asset.format("" if not mw_settings.MINIFED else ".min")


class GooglePointFieldWidget(BaseGeometryWidget):
    template_name = "mapwidgets/google-point-field-widget.html"

    @property
    def media(self):
        css = {
            "all": [
                minify_if_not_debug("mapwidgets/css/map_widgets{}.css"),
            ]
        }

        js = [
            "https://maps.googleapis.com/maps/api/js?libraries=places&key={}".format(mw_settings.GOOGLE_MAP_API_KEY)
        ]

        if not mw_settings.MINIFED:
            js = js + [
                "mapwidgets/js/jquery_class.js",
                "mapwidgets/js/django_mw_base.js",
                "mapwidgets/js/mw_google_point_field.js",
            ]
        else:
            js = js + [
                "mapwidgets/js/mw_google_point_inline_field.min.js"
            ]

        return forms.Media(js=js, css=css)

    @staticmethod
    def map_options():
        return json.dumps(mw_settings.GooglePointFieldWidget)

    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = dict()

        field_value = {}
        if isinstance(value,  Point):
            field_value["lng"] = value.x
            field_value["lat"] = value.y

        if value and isinstance(value, six.string_types):
            coordinates = self.deserialize(value)
            field_value["lng"] = getattr(coordinates, "x", None)
            field_value["lat"] = getattr(coordinates, "y", None)

        extra_attrs = {
            "options": self.map_options(),
            "field_value": json.dumps(field_value)
        }

        attrs.update(extra_attrs)
        return super(GooglePointFieldWidget, self).render(name, value, attrs)


class PointFieldInlineWidgetMixin(object):

    def get_js_widget_data(self, name, element_id):
        map_elem_selector = "#%s-mw-wrap" % name
        map_elem_id = "%s-map-elem" % name
        google_auto_input_id = "%s-mw-google-address-input" % name
        location_input_id = "#%s" % element_id
        js_widget_params = {
            "wrapElemSelector": map_elem_selector,
            "mapElemID": map_elem_id,
            "googleAutoInputID": google_auto_input_id,
            "locationInputID": location_input_id
        }
        return js_widget_params


class GooglePointFieldInlineWidget(PointFieldInlineWidgetMixin, GooglePointFieldWidget):
    template_name = "mapwidgets/google-point-field-inline-widget.html"

    @property
    def media(self):
        css = {
            "all": [
                minify_if_not_debug("mapwidgets/css/map_widgets{}.css"),
            ]
        }

        js = [
            "https://maps.googleapis.com/maps/api/js?libraries=places&key={}".format(mw_settings.GOOGLE_MAP_API_KEY)
        ]

        if not mw_settings.MINIFED:
            js = js + [
                "mapwidgets/js/jquery_class.js",
                "mapwidgets/js/django_mw_base.js",
                "mapwidgets/js/mw_google_point_field.js",
                "mapwidgets/js/mw_google_point_field_generater.js"
            ]
        else:
            js = js + [
                "mapwidgets/js/mw_google_point_inline_field.min.js"
            ]

        return forms.Media(js=js, css=css)

    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = dict()

        element_id = attrs.get("id")
        is_formset_empty_from_template = "__prefix__" in element_id
        widget_data = self.get_js_widget_data(name, element_id)
        attrs.update({
            "js_widget_data": json.dumps(widget_data),
            "is_formset_empty_from_template": is_formset_empty_from_template
        })
        return super(GooglePointFieldInlineWidget, self).render(name, value, attrs)


class BaseStaticMapWidget(forms.Widget):
    template_name = None

    @property
    def map_settings(self):
        raise NotImplementedError('subclasses of BaseStaticMapWidget must provide a map_settings method')

    @property
    def marker_settings(self):
        raise NotImplementedError('subclasses of BaseStaticMapWidget must provide a marker_settings method')

    def get_template(self):
        if self.template_name is None:
            raise ImproperlyConfigured('BaseStaticMapWidget requires either a definition of "template_name"')
        return self.template_name

    def get_image_url(self, value):
        raise NotImplementedError('subclasses of BaseStaticMapWidget must provide a get_map_image_url method')

    def get_context_data(self, name, value, attrs):
        return {
            "image_url": self.get_image_url(value),
            "name": name,
            "value": value or "",
            "attrs": attrs
        }

    def render(self, name, value, attrs=None):
        context = self.get_context_data(name, value, attrs)
        template = self.get_template()
        return render_to_string(template, context)


class GoogleStaticMapWidget(BaseStaticMapWidget):
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    settings = mw_settings.GoogleStaticMapWidget
    template_name = "mapwidgets/google-static-map.html"

    def __init__(self, zoom=None, size=None, *args, **kwargs):
        self.zoom = zoom
        self.size = size
        super(GoogleStaticMapWidget, self).__init__(*args, **kwargs)

    @property
    def map_settings(self):
        self.settings["key"] = mw_settings.GOOGLE_MAP_API_KEY
        if mw_settings.GOOGLE_MAP_API_SIGNATURE:
            self.settings["signature"] = mw_settings.GOOGLE_MAP_API_SIGNATURE
        if self.size:
            self.settings["size"] = self.size
            self.settings["zoom"] = self.zoom
        return self.settings

    @property
    def marker_settings(self):
        if not isinstance(mw_settings.GoogleStaticMapMarkerSettings, dict):
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


class GoogleStaticOverlayMapWidget(GoogleStaticMapWidget):
    settings = mw_settings.GoogleStaticOverlayMapWidget
    template_name = "mapwidgets/google-static-overlay-map.html"

    class Media:
        css = {
            "all": (
                minify_if_not_debug("mapwidgets/css/magnific-popup{}.css"),
            )
        }

        js = (
            minify_if_not_debug("mapwidgets/js/jquery.custom.magnific-popup{}.js"),
        )

    def __init__(self, zoom=None, size=None, thumbnail_size=None, *args, **kwargs):
        self.thumbnail_size = thumbnail_size
        super(GoogleStaticOverlayMapWidget, self).__init__(zoom, size, *args, **kwargs)

    @property
    def map_settings(self):
        settings = super(GoogleStaticOverlayMapWidget, self).map_settings
        if self.thumbnail_size:
            settings["thumbnail_size"] = self.thumbnail_size
        return settings

    def thumbnail_url(self, value):
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
        context = super(GoogleStaticOverlayMapWidget, self).get_context_data(name, value, attrs)
        context["thumbnail_url"] = self.thumbnail_url(value)
        return context
