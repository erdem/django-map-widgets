import json

from django.contrib.gis.forms import BaseGeometryWidget
from django.contrib.gis.geos import Point
from django.core.exceptions import ImproperlyConfigured

from mapwidgets.settings import mw_settings


class GoogleMapWidget(BaseGeometryWidget):
    template_name = "mapwidgets/google-map-widget.html"

    class Media:
        css = {
            "all": (
                "mapwidgets/css/map_widgets.css",
                )
        }

        js = (
            "https://maps.googleapis.com/maps/api/js?libraries=places&key=%s" % mw_settings.GOOGLE_MAP_API_KEY,
            "https://code.jquery.com/jquery-1.11.3.min.js",
            "mapwidgets/js/jquery_class.min.js",
            "mapwidgets/js/django_mw_base.js",
            "mapwidgets/js/django_mw_google_map.js",
        )

    @staticmethod
    def map_options():
        return json.dumps(mw_settings.map_conf)



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
        return super(GoogleMapWidget, self).render(name, value, attrs)


class InlineMapWidgetMixin(object):
    inline_add_row_jquery_selector = None

    def map_options(self):
        if not self.inline_add_row_jquery_selector:
            raise ImproperlyConfigured(
                "The '%s' does not specify "
                "a 'inline_add_row_jquery_selector'." % self.__class__.__name__)

        map_conf = mw_settings.map_conf
        map_conf["inline_add_row_jquery_selector"] = self.inline_add_row_jquery_selector
        return json.dumps(mw_settings.map_conf)


class GoogleInlineMapWidget(InlineMapWidgetMixin, GoogleMapWidget):
    inline_add_row_jquery_selector = None
    template_name = "mapwidgets/google-inline-map-widget.html"


    class Media:
        css = {
            "all": (
                "mapwidgets/css/map_widgets.css",
            )
        }

        js = (
            "https://maps.googleapis.com/maps/api/js?libraries=places&key=%s" % mw_settings.GOOGLE_MAP_API_KEY,
            "https://code.jquery.com/jquery-1.11.3.min.js",  # todo optional
            "mapwidgets/js/jquery_class.min.js",
            "mapwidgets/js/django_mw_base.js",
            "mapwidgets/js/django-mw-generater.js",
            "mapwidgets/js/django_mw_google_map.js",
        )


class DjangoAdminInlineGoogleMapWidget(GoogleInlineMapWidget):
    inline_add_row_jquery_selector = ".inline-group .add-row a"
