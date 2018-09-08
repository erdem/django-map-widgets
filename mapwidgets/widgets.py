import json

from django import forms
from django.contrib.gis.forms import BaseGeometryWidget
from django.contrib.gis.geos import Point
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils import six
from django.utils.http import urlencode

from mapwidgets.constants import STATIC_MAP_PLACEHOLDER_IMAGE
from mapwidgets.settings import MapWidgetSettings, mw_settings


def minify_if_not_debug(asset):
    """
        Transform template string `asset` by inserting '.min' if DEBUG=False
    """
    return asset.format("" if not mw_settings.MINIFED else ".min")


class BasePointFieldMapWidget(BaseGeometryWidget):
    settings_namespace = None
    settings = None

    def __init__(self, *args, **kwargs):
        attrs = kwargs.get("attrs")
        self.attrs = {}
        for key in ('geom_type', 'map_srid', 'map_width', 'map_height', 'display_raw'):
            if key in kwargs:
                self.attrs[key] = kwargs.get(key)
            else:
                self.attrs[key] = getattr(self, key)

        if isinstance(attrs, dict):
            self.attrs.update(attrs)

        self.custom_settings = False
        if kwargs.get("settings"):
            self.settings = kwargs.pop("settings")
            self.custom_settings = True

    def map_options(self):
        if not self.settings:  # pragma: no cover
            raise ImproperlyConfigured('%s requires either a definition of "settings"' % self.__class__.__name__)

        if not self.settings_namespace:  # pragma: no cover
            raise ImproperlyConfigured('%s requires either a definition of "settings_namespace"' % self.__class__.__name__)

        if self.custom_settings:
            custom_settings = MapWidgetSettings(app_settings=self.settings)
            return json.dumps(getattr(custom_settings, self.settings_namespace))
        return json.dumps(self.settings)


class GooglePointFieldWidget(BasePointFieldMapWidget):
    template_name = "mapwidgets/google-point-field-widget.html"
    settings = mw_settings.GooglePointFieldWidget
    settings_namespace = "GooglePointFieldWidget"
    google_map_srid = 4326

    @property
    def media(self):
        css = {
            "all": [
                minify_if_not_debug("mapwidgets/css/map_widgets{}.css"),
            ]
        }

        js = [
            "https://code.jquery.com/jquery-3.3.1.slim.min.js",
            "https://maps.googleapis.com/maps/api/js?libraries=places&language={}&key={}".format(
                mw_settings.LANGUAGE, mw_settings.GOOGLE_MAP_API_KEY
            )
        ]

        if not mw_settings.MINIFED:  # pragma: no cover
            js = js + [
                "mapwidgets/js/jquery_class.js",
                "mapwidgets/js/django_mw_base.js",
                "mapwidgets/js/mw_google_point_field.js",
            ]
        else:
            js = js + [
                "mapwidgets/js/mw_google_point_field.min.js"
            ]

        return forms.Media(js=js, css=css)

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = dict()

        field_value = {}
        if value and isinstance(value, six.string_types):
            value = self.deserialize(value)
            longitude, latitude = value.coords
            field_value["lng"] = longitude
            field_value["lat"] = latitude

        if isinstance(value,  Point):
            if value.srid and value.srid != self.google_map_srid:
                ogr = value.ogr
                ogr.transform(self.google_map_srid)
                value = ogr

            longitude, latitude = value.coords
            field_value["lng"] = longitude
            field_value["lat"] = latitude

        extra_attrs = {
            "options": self.map_options(),
            "field_value": json.dumps(field_value)
        }
        attrs.update(extra_attrs)
        self.as_super = super(GooglePointFieldWidget, self)
        if renderer is not None:
            return self.as_super.render(name, value, attrs, renderer)
        else:
            return self.as_super.render(name, value, attrs)


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

    def render(self, name, value, attrs=None, renderer=None):
        if not attrs:
            attrs = dict()

        element_id = attrs.get("id")
        is_formset_empty_form_template = "__prefix__" in name
        widget_data = self.get_js_widget_data(name, element_id)
        attrs.update({
            "js_widget_data": json.dumps(widget_data),
            "is_formset_empty_form_template": is_formset_empty_form_template
        })
        self.as_super = super(PointFieldInlineWidgetMixin, self)
        if renderer is not None:
            return self.as_super.render(name, value, attrs, renderer)
        else:
            return self.as_super.render(name, value, attrs)


class GooglePointFieldInlineWidget(PointFieldInlineWidgetMixin, GooglePointFieldWidget):
    template_name = "mapwidgets/google-point-field-inline-widget.html"
    settings = mw_settings.GooglePointFieldWidget
    settings_namespace = "GooglePointFieldWidget"

    @property
    def media(self):
        css = {
            "all": [
                minify_if_not_debug("mapwidgets/css/map_widgets{}.css"),
            ]
        }

        js = [
            "https://code.jquery.com/jquery-3.3.1.slim.min.js",
            "https://maps.googleapis.com/maps/api/js?libraries=places&language={}&key={}".format(
                mw_settings.LANGUAGE, mw_settings.GOOGLE_MAP_API_KEY
            )
        ]

        if not mw_settings.MINIFED:  # pragma: no cover
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


class BaseStaticMapWidget(forms.Widget):
    template_name = None

    @property
    def map_settings(self):  # pragma: no cover
        raise NotImplementedError('subclasses of BaseStaticMapWidget must provide a map_settings method')

    @property
    def marker_settings(self):  # pragma: no cover
        raise NotImplementedError('subclasses of BaseStaticMapWidget must provide a marker_settings method')

    def get_template(self):  # pragma: no cover
        if self.template_name is None:
            raise ImproperlyConfigured('BaseStaticMapWidget requires either a definition of "template_name"')
        return self.template_name

    def get_image_url(self, value):  # pragma: no cover
        raise NotImplementedError('subclasses of BaseStaticMapWidget must provide a get_map_image_url method')

    def get_context_data(self, name, value, attrs):
        return {
            "image_url": self.get_image_url(value),
            "name": name,
            "value": value or "",
            "attrs": attrs
        }

    def render(self, name, value, attrs=None, renderer=None):
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
            "https://code.jquery.com/jquery-3.3.1.slim.min.js",
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
        context = super(GoogleStaticOverlayMapWidget, self).get_context_data(name, value, attrs)
        context["thumbnail_url"] = self.get_thumbnail_url(value)
        return context
