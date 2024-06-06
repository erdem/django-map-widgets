import json

from django.contrib.gis import forms
from django.contrib.gis.geos import GEOSGeometry

from mapwidgets.settings import mw_settings


class SettingsMixin:
    _settings = None

    def __init__(self, *args, **kwargs):
        self.custom_settings = kwargs.pop("settings", None)
        super().__init__(*args, **kwargs)

    @property
    def settings(self):
        _settings = self._settings.copy()
        if self.custom_settings is not None:
            assert isinstance(
                self.custom_settings, dict
            ), "`settings` argument must be a dict type"
            _settings.update(self.custom_settings)

        return _settings


class BasePointFieldInteractiveWidget(forms.BaseGeometryWidget, SettingsMixin):
    _settings = None
    map_srid = mw_settings.srid

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


class BaseStaticWidget(forms.Widget, SettingsMixin):
    template_name = "mapwidgets/static_widget.html"
    base_url = None

    def __init__(self, image_url_params=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_url_params = {} if image_url_params is None else image_url_params.copy()


    def get_base_url(self):
        if not self.base_url:
            raise ValueError("`base_url` must be set")
        return self.base_url

    def get_static_image_url_params(self, coordinates, **kwargs):
        raise NotImplementedError(
            "subclasses of BaseStaticMapWidget must provide a get_map_image_url method"
        )

    def get_static_image_url(self, value, **kwargs):  # pragma: no cover
        raise NotImplementedError(
            "subclasses of BaseStaticMapWidget must provide a get_map_image_url method"
        )

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["image_url"] = self.get_static_image_url(value)
        return context

