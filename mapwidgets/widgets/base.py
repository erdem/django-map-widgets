import json

from django import forms
from django.contrib.gis.forms import BaseGeometryWidget
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings as django_settings

from mapwidgets.settings import mw_settings


class BasePointFieldWidget(BaseGeometryWidget):
    _settings = None
    map_srid = mw_settings.srid

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_settings = kwargs.pop("settings", None)

    @property
    def settings(self):
        return self._settings

    def get_css_paths(self, extra_css=None, minified=False):
        extra_css = extra_css or []
        media_settings = self.settings.media
        return extra_css + (
            media_settings.css.minified if minified else media_settings.css.dev
        )

    def get_js_paths(self, extra_js=None, minified=False):
        extra_js = extra_js or []
        media_settings = self.settings.media
        return extra_js + (
            media_settings.js.minified if minified else media_settings.js.dev
        )

    def _media(self, extra_css=None, extra_js=None):
        css_paths = self.get_css_paths(extra_css, minified=not mw_settings.is_dev_mode)
        js_paths = self.get_js_paths(extra_js, minified=not mw_settings.is_dev_mode)
        return forms.Media(css={"all": css_paths}, js=js_paths)

    @property
    def media(self):
        return self._media()

    def geos_to_dict(self, geom: GEOSGeometry):
        if geom is None:
            return None

        geom_dict = {
            "srid": geom.srid,
            "wkt": str(geom),
            "coords": geom.coords,
            "geom_type": geom.geom_type,
        }
        longitude, latitude = geom.coords

        # Transform the coordinates for backwards compatibility
        geom_dict["lng"] = longitude
        geom_dict["lat"] = latitude
        return geom_dict

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        field_value = context["serialized"]
        if field_value:
            field_value = self.geos_to_dict(self.deserialize(field_value))
        else:
            field_value = None

        extra_context = {
            "options": json.dumps(self.settings),
            "field_value": json.dumps(field_value),
        }
        context.update(extra_context)
        return context
