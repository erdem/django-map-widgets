from django.core.exceptions import ImproperlyConfigured
from django.utils.http import urlencode

from mapwidgets.settings import mw_settings
from mapwidgets.widgets.base import BasePointFieldInteractiveWidget, BaseStaticWidget


class MapboxPointFieldWidget(BasePointFieldInteractiveWidget):
    template_name = "mapwidgets/pointfield/mapbox/interactive.html"
    _settings = mw_settings.Mapbox.PointField.interactive

    @property
    def settings(self):
        settings = super().settings
        if not mw_settings.Mapbox.accessToken:
            raise ImproperlyConfigured(
                "`Mapbox.accessToken` setting is required to use Mapbox widgets."
            )
        settings["accessToken"] = mw_settings.Mapbox.accessToken
        return settings

    @property
    def media(self):
        return self._media(
            extra_js=[
                "https://api.mapbox.com/mapbox-gl-js/v3.3.0/mapbox-gl.js",
                "https://unpkg.com/@mapbox/mapbox-sdk/umd/mapbox-sdk.min.js",
                "https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.7.2/mapbox-gl-geocoder.min.js",
            ],
            extra_css=[
                "https://api.mapbox.com/mapbox-gl-js/v3.3.0/mapbox-gl.css",
                "https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.7.2/mapbox-gl-geocoder.css",
            ],
        )


class MapboxPointFieldStaticWidget(BaseStaticWidget):
    _base_url = "https://api.mapbox.com/styles/v1/"
    _settings = mw_settings.Mapbox.PointField.static
    # https://docs.mapbox.com/api/maps/static-images/#retrieve-a-static-map-from-a-style
    _url_params_template = "{username}/{style_id}/static/{overlay}/{lon},{lat},{zoom},{bearing},{pitch}/{width}x{height}{@2x}"
    # https://docs.mapbox.com/api/maps/static-images/#marker
    _overlay_template = "{name}-{label}+{color}({lon},{lat})"

    def get_image_url_params(self, coordinates):
        if not mw_settings.Mapbox.accessToken:
            raise ImproperlyConfigured(
                "`Mapbox.accessToken` setting is required to use Mapbox widgets."
            )

        return {
            "access_token": mw_settings.Mapbox.accessToken,
        }

    def get_overlay(self, lon, lat, name=None, label=None, color=None):
        overlay_template = f"{name}"

        if label:
            overlay_template += f"-{label}"

        if color:
            overlay_template += f"+{color}"

        overlay_template += f"({lon},{lat})"

        return "".join(overlay_template)

    def get_image_url(self, coordinates, **extraMapParams):
        query_strings = urlencode(self.get_image_url_params(coordinates))
        longitude, latitude = coordinates.x, coordinates.y
        overlay = self.get_overlay(
            lon=longitude, lat=latitude, **self.settings.overlayParams
        )
        self.settings.mapParams.update(extraMapParams)
        url_params = self._url_params_template.format(
            overlay=overlay, lon=longitude, lat=latitude, **self.settings.mapParams
        )
        return f"{self._base_url}{url_params}?{query_strings}"

    def get_thumbnail_url_params(self, coordinates):
        return self.get_image_url_params(coordinates)

    def get_thumbnail_url(self, coordinates):
        if self.settings.thumbnailSize:
            thumbnail_width, thumbnail_height = self.settings.thumbnailSize.split("x")
            return self.get_image_url(
                coordinates, width=thumbnail_width, height=thumbnail_height
            )
        return self.get_image_url(coordinates)

    def get_html_image_tag_attrs(self):
        if self.settings.thumbnailSize:
            widget, height = self.settings.thumbnailSize.split("x")
        elif self.settings.mapParams.width and self.settings.mapParams.height:
            widget, height = (
                self.settings.mapParams.width,
                self.settings.mapParams.height,
            )
        else:
            widget, height = self.DEFAULT_IMAGE_SIZE.split("x")
        return {"width": widget, "height": height}
