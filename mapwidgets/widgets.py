import json

from django import forms
from django.contrib.gis.forms import BaseGeometryWidget
from django.contrib.gis.geos import Point
from django.template.loader import render_to_string

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


class ReadOnlyWidgetBase(forms.Widget):
    template_name = "mapwidgets/read-only-widget.html"

    def __init__(self, attrs=None, *args, **kwargs):
        self.marker_label = kwargs.get("marker_label", "")
        super(ReadOnlyWidgetBase, self).__init__(attrs)

    @property
    def map_settings(self):
        return mw_settings.GoogleStaticMapWidget

    @property
    def marker_settings(self):
        return mw_settings.GoogleStaticMapMarkerSettings

    def get_image_url(self, value):
        raise NotImplementedError('subclasses of ReadOnlyWidgetBase must provide a get_map_image_url method')

    def render(self, name, value, attrs=None):
        context = {
            "image_url": self.get_static_map_image_url(value),
            "name": name,
            "value": value,
            "attrs": attrs
        }
        return render_to_string(self.template_name, context)


class GooglePointFieldReadOnlyWidget(ReadOnlyWidgetBase):

    def get_image_url(self, value):
        if isinstance(value, Point):
            longitude, latitude = value.x, value.y

        return None


