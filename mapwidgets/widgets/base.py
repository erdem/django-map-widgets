import json

from django import forms
from django.contrib.gis.forms import BaseGeometryWidget
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string

from mapwidgets.settings import MapWidgetSettings, mw_settings


class BasePointFieldWidget(BaseGeometryWidget):
    settings_namespace = None
    settings = None
    map_srid = mw_settings.srid

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_settings = kwargs.pop('settings', None)

    def _map_options(self):
        if not self.settings or not self.settings_namespace:
            raise ImproperlyConfigured(f'{self.__class__.__name__} requires "settings" and "settings_namespace" to be defined')

        if self.custom_settings:
            custom_settings = MapWidgetSettings(app_settings=self.custom_settings)
            self.settings = getattr(custom_settings, self.settings_namespace)
        return self.settings.dict()

    def generate_media(self, js_sources, css_files, min_js, dev_js):
        suffix = '.min' if mw_settings.MINIFED else ''
        css_files = [css_file.format(suffix) for css_file in css_files]
        js_files = js_sources + ([min_js] if mw_settings.MINIFED else dev_js)
        css = {'all': css_files}
        return forms.Media(js=js_files, css=css)

    def geos_to_dict(self, geom: GEOSGeometry):
        if geom is None:
            return None

        geom_dict = {
            'srid': geom.srid,
            'wkt': str(geom),
            'coords': geom.coords,
            'geom_type': geom.geom_type,
        }
        longitude, latitude = geom.coords

        # Transform the coordinates for backwards compatibility
        geom_dict['lng'] = longitude
        geom_dict['lat'] = latitude
        return geom_dict

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        de_value = self.deserialize(context["serialized"])
        extra_context = {
            'options': json.dumps(self._map_options()),
            'field_value': json.dumps(self.geos_to_dict(de_value))
        }
        context.update(extra_context)
        return context


class BasePointFieldStaticWidget(forms.Widget):
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
