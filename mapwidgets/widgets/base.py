import json

from django import forms
from django.contrib.gis.forms import BaseGeometryWidget
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ImproperlyConfigured

from mapwidgets.settings import MapWidgetSettings, mw_settings


class BasePointFieldWidget(BaseGeometryWidget):
    settings_namespace = None
    settings = None
    map_srid = mw_settings.srid

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_settings = kwargs.pop("settings", None)

    def _map_options(self):
        if not self.settings or not self.settings_namespace:
            raise ImproperlyConfigured(
                f'{self.__class__.__name__} requires "settings" and "settings_namespace" to be defined'
            )

        if self.custom_settings:
            custom_settings = MapWidgetSettings(app_settings=self.custom_settings)
            self.settings = getattr(custom_settings, self.settings_namespace)
        return self.settings

    def generate_media(self, js_sources, css_files, min_js, dev_js):
        suffix = ".min" if mw_settings.MINIFED else ""
        css_files = [css_file.format(suffix) for css_file in css_files]
        js_files = js_sources + ([min_js] if mw_settings.MINIFED else dev_js)
        css = {"all": css_files}
        return forms.Media(js=js_files, css=css)

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
            "options": json.dumps(self._map_options()),
            "field_value": json.dumps(field_value),
        }
        context.update(extra_context)
        return context
