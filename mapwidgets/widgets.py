from django.conf import settings
from django.contrib.gis.forms import BaseGeometryWidget

from mapwidgets.utils import get_map_options


class GoogleMapWidget(BaseGeometryWidget):
    template_name = "mapwidgets/google-map-widget.html"

    class Media:
        css = {
            "all": (
                "mapwidgets/css/map_widgets.css",
                )
        }

        js = (
            "https://maps.googleapis.com/maps/api/js?libraries=places",
            "https://code.jquery.com/jquery-1.11.3.min.js",
            "mapwidgets/js/jquery_class.min.js",
            "mapwidgets/js/django_mw_base.js",
            "mapwidgets/js/django_mw_google_map.js",
        )

    def render(self, name, value, attrs=None):
        attrs = {
            "name": name,
            "value": value,
            "widget": self,
            "options": get_map_options(),
            "STATIC_URL": settings.STATIC_URL,
            "textarea_attrs": attrs
        }
        return super(GoogleMapWidget, self).render(name, value, attrs)