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

    def dev_media(self, extra_css: list = None, extra_js=None):
        _js = extra_js or []
        _css = extra_css or []
        _js.extend(self.settings.media.js.dev)
        _css.extend(self.settings.media.css.dev)
        return dict(css=_css, js=_js)

    def minified_media(self, extra_css=None, extra_js=None):
        _js = extra_js or []
        _css = extra_css or []
        _js.extend(self.settings.media.js.minified)
        _css.extend(self.settings.media.css.minified)
        return dict(css=_css, js=_js)

    def _media(self, extra_css=None, extra_js=None):
        media_paths = self.dev_media(extra_css, extra_js)
        if not django_settings.DEBUG:
            media_paths = self.minified_media(extra_css, extra_js)
        return forms.Media(css={"all": media_paths["css"]}, js=media_paths["js"])

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
