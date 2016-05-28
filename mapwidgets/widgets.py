import json

from django.contrib.gis.forms import BaseGeometryWidget
from django.contrib.gis.geos import Point

from mapwidgets.utils import get_map_options, get_google_api_key


class GoogleMapWidget(BaseGeometryWidget):
    template_name = "mapwidgets/google-map-widget.html"

    class Media:
        css = {
            "all": (
                "mapwidgets/css/map_widgets.css",
                )
        }

        js = (
            "https://maps.googleapis.com/maps/api/js?libraries=places&key=%s" % get_google_api_key(),
            "https://code.jquery.com/jquery-1.11.3.min.js",
            "mapwidgets/js/jquery_class.min.js",
            "mapwidgets/js/django_mw_base.js",
            "mapwidgets/js/django_mw_google_map.js",
        )

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
            "options": get_map_options(),
            "field_value": json.dumps(field_value)
        }

        attrs.update(extra_attrs)
        return super(GoogleMapWidget, self).render(name, value, attrs)