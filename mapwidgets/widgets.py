import json

from django import forms
from django.contrib.gis.forms import BaseGeometryWidget
from django.contrib.gis.geos import Point
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.http import urlencode

from mapwidgets.constants import STATIC_MAP_PLACEHOLDER_IMAGE
from mapwidgets.settings import mw_settings


class GooglePointFieldWidget(BaseGeometryWidget):
    template_name = "mapwidgets/google-point-field-widget.html"

    class Media:
        css = {
            "all": (
                "mapwidgets/css/map_widgets.css",
                )
        }

        js = (
            "https://maps.googleapis.com/maps/api/js?libraries=places&key=%s" % mw_settings.GOOGLE_MAP_API_KEY,
            "mapwidgets/js/jquery_class.min.js",
            "mapwidgets/js/django_mw_base.js",
            "mapwidgets/js/mw_google_point_field.js",
        )

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

        if value and isinstance(value, basestring):
            coordinates = self.deserialize(value)
            field_value["lng"] = coordinates.x
            field_value["lat"] = coordinates.y

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

    class Media:
        css = {
            "all": (
                "mapwidgets/css/map_widgets.css",
            )
        }

        js = (
            "https://maps.googleapis.com/maps/api/js?libraries=places&key=%s" % mw_settings.GOOGLE_MAP_API_KEY,
            "mapwidgets/js/jquery_class.min.js",
            "mapwidgets/js/django_mw_base.js",
            "mapwidgets/js/mw_google_point_field.js",
            "mapwidgets/js/mw_google_point_field_generater.js",
        )

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

    @property
    def map_settings(self):
        raise NotImplementedError('subclasses of BaseStaticMapWidget must provide a map_settings method')

    @property
    def marker_settings(self):
        raise NotImplementedError('subclasses of BaseStaticMapWidget must provide a marker_settings method')

    def get_template(self):
        raise NotImplementedError('subclasses of BaseStaticMapWidget must provide a get_template_name method')

    def get_image_url(self, value):
        raise NotImplementedError('subclasses of BaseStaticMapWidget must provide a get_map_image_url method')

    def get_context_data(self, name, value, attrs):
        return {
            "image_url": self.get_image_url(value),
            "name": name,
            "value": value,
            "attrs": attrs
        }

    def render(self, name, value, attrs=None):
        context = self.get_context_data(name, value, attrs)
        template = self.get_template()
        return format_html(template, **context)


class GoogleStaticMapWidget(BaseStaticMapWidget):
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    settings = mw_settings.GoogleStaticMapWidget

    @property
    def map_settings(self):
        self.settings["api_key"] = mw_settings.GOOGLE_MAP_API_KEY
        self.settings["api_signature"] = mw_settings.GOOGLE_MAP_API_SIGNATURE
        return self.settings

    @property
    def marker_settings(self):
        if not isinstance(mw_settings.GoogleStaticMapMarkerSettings, dict):
            raise TypeError('GoogleStaticMapMarkerSettings must be a dictionary.')
        return mw_settings.GoogleStaticMapMarkerSettings

    def get_template(self):
        return '<a href="{image_url}" target="_blank" class="static-map-link"><img src="{image_url}"></a>'

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

    class Media:
        css = {
            "all": (
                "mapwidgets/css/magnific-popup.css",
            )
        }

        js = (
            "mapwidgets/js/custom.jquery.magnific-popup.min.js",
        )

    def get_template(self):
        return '<a href="{image_url}" class="map-widget-overlay-link"><img src="{thumbnail_url}"></a>'

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
