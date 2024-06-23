import json

from django.contrib.gis import forms
from django.contrib.gis.geos import GEOSGeometry
from django.utils.http import urlencode

from mapwidgets.settings import mw_settings
from mapwidgets.widgets.mixins import SettingsMixin


class BasePointFieldInteractiveWidget(SettingsMixin, forms.BaseGeometryWidget):
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


class BaseStaticWidget(SettingsMixin, forms.TextInput):
    template_name = "mapwidgets/static_widget.html"
    _base_url = None
    DEFAULT_IMAGE_SIZE = "240x240"

    @property
    def media(self):
        if self.settings.enableMagnificPopup:
            return forms.Media(
                css={"all": ["mapwidgets/css/magnific-popup.min.css"]},
                js=["mapwidgets/js/staticmap/mw_jquery.magnific-popup.min.js"],
            )
        return forms.Media()

    def sign_url(self, url):
        """
        Sign url with a secret.
        """
        return url

    @property
    def base_url(self):
        if not self._base_url:
            raise ValueError("`_base_url` attribute must be set")
        return self._base_url

    def get_image_url_params(self, coordinates):
        raise NotImplementedError(
            "subclasses of BaseStaticMapWidget must provide a get_image_url_params method"
        )

    def get_thumbnail_url_params(self, coordinates):
        params = self.get_image_url_params(coordinates)
        if self.settings.thumbnailSize:
            params["size"] = self.settings.thumbnailSize
        return params

    def get_image_url(self, coordinates):
        return f"{self.base_url}?{urlencode(self.get_image_url_params(coordinates))}"

    def get_html_image_tag_attrs(self):
        if self.settings.thumbnailSize:
            widget, height = self.settings.thumbnailSize.split("x")
        elif self.settings.mapParams.size:
            widget, height = self.settings.mapParams.size.split("x")
        else:
            widget, height = self.DEFAULT_IMAGE_SIZE.split("x")
        return {"width": widget, "height": height}

    def get_thumbnail_url(self, value):
        return f"{self.base_url}?{urlencode(self.get_thumbnail_url_params(value))}"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if value:
            context["image_url"] = self.sign_url(self.get_image_url(value))
            context["is_magnific_popup_enabled"] = self.settings.enableMagnificPopup
            context["image_tag_attrs"] = self.get_html_image_tag_attrs()
            if self.settings.thumbnailSize:
                context["thumbnail_url"] = self.sign_url(self.get_thumbnail_url(value))
            else:
                context["thumbnail_url"] = context["image_url"]

        return context
