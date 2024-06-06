from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.utils.http import urlencode

from mapwidgets.settings import mw_settings
from mapwidgets.utils import AsyncJS
from mapwidgets.widgets.base import BasePointFieldInteractiveWidget
from mapwidgets.widgets.mixins import PointFieldInlineWidgetMixin


class GoogleMapPointFieldWidget(BasePointFieldInteractiveWidget):
    template_name = "mapwidgets/pointfield/googlemap/interactive.html"
    _settings = mw_settings.GoogleMap.PointField.interactive

    @property
    def _google_map_js_url(self):
        if mw_settings.GoogleMap.apiKey is None:
            raise ImproperlyConfigured(
                "`GoogleMap.apiKey` setting is required to use Google Map widgets."
            )
        cdn_url_params = {
            "key": mw_settings.GoogleMap.apiKey,
            "callback": "googleMapWidgetsCallback",
        }
        cdn_url_params.update(mw_settings.GoogleMap["CDNURLParams"])
        return f"https://maps.googleapis.com/maps/api/js?{urlencode(cdn_url_params)}"

    @property
    def media(self):
        return self._media(extra_js=[AsyncJS(self._google_map_js_url)])


class GoogleMapPointFieldInlineWidget(
    GoogleMapPointFieldWidget, PointFieldInlineWidgetMixin
):
    template_name = "mapwidgets/pointfield/googlemap/interactive_inline.html"
    _settings = mw_settings.GoogleMap.PointField.interactive

    def get_js_paths(self, extra_js=None, minified=False):
        js_paths = super().get_js_paths(extra_js, minified)

        if minified:
            js_paths = [
                AsyncJS(self._google_map_js_url),
                "mapwidgets/js/pointfield/interactive/googlemap/mw_pointfield_inline.min.js",
            ]
        else:
            inline_generator_js = "mapwidgets/js/pointfield/interactive/googlemap/mw_pointfield_inline_generator.js"
            js_paths.append(inline_generator_js)

        return js_paths


class GoogleMapPointFieldStaticWidget(BaseStaticWidget):
    _base_url = "https://maps.googleapis.com/maps/api/staticmap"
    _settings = mw_settings.GoogleMap.PointField.static

    # !/usr/bin/python
    # -*- coding: utf-8 -*-
    """ Signs a URL using a URL signing secret """

    import hashlib
    import hmac
    import base64
    import urllib.parse as urlparse

    def sign_url(self, url=None, secret=None):
        """
        Sign a GoogleMap Static API request URL with a URL signing secret.
        https://developers.google.com/maps/documentation/maps-static/digital-signature#sample-code-for-url-signing
        """
        if not url or not secret:
            raise ValueError("Both input_url and secret are required")

        url = urlparse.urlparse(url)

        # We only need to sign the path+query part of the string
        url_to_sign = url.path + "?" + url.query

        # Decode the private key into its binary format
        # We need to decode the URL-encoded private key
        decoded_key = base64.urlsafe_b64decode(secret)

        # Create a signature using the private key and the URL-encoded
        # string using HMAC SHA1. This signature will be binary.
        signature = hmac.new(decoded_key, str.encode(url_to_sign), hashlib.sha1)

        # Encode the binary signature into base64 for use within a URL
        encoded_signature = base64.urlsafe_b64encode(signature.digest())

        original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

        # Return signed URL
        return original_url + "&signature=" + encoded_signature.decode()

    def get_static_image_url_params(self, coordinates):
        params = {
            "key": mw_settings.GoogleMap.apiKey,
        }
