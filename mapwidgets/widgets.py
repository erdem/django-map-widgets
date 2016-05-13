from django import forms
from django.conf import settings
from django.contrib.gis.forms import BaseGeometryWidget
from django.template.loader import render_to_string


class GoogleMapWidget(forms.Textarea):
    template = "mapwidgets/google-map-widget.html"

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
        textarea = super(GoogleMapWidget, self).render(name, value, attrs)
        data = {
            "textarea": textarea,
            "name": name,
            "value": value,
            "widget": self,
            "options": "{}",
            "STATIC_URL": settings.STATIC_URL,
            "textarea_attrs": attrs
        }
        return render_to_string(self.template, data)