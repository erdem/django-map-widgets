import json

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings

from selenium import webdriver

import mapwidgets
from mapwidgets import GooglePointFieldWidget


from mixins import SeleniumScreenShotMixin

DEFAULT_GOOGLE_POINT_MAP_CENTER_LOCATION = (51.5073509, -0.12775829999998223)
DEFAULT_GOOGLE_POINT_MAP_ZOOM = 15
GOOGLE_MAP_API_KEY = "AIzaSyC6BeCYCBSWDdC3snYRFKWw18bd9MA-uu4"


MAP_WIDGETS = {
    "GooglePointFieldWidget": (
        ("zoom", DEFAULT_GOOGLE_POINT_MAP_ZOOM),
        ("mapCenterLocation", DEFAULT_GOOGLE_POINT_MAP_CENTER_LOCATION),
        ("markerFitZoom", 11),
        ("GooglePlaceAutocompleteOptions", {'componentRestrictions': {'country': 'uk'}})
    )
}


class GooglePointWidgetUnitTests(TestCase):

    @override_settings(MAP_WIDGETS=MAP_WIDGETS)
    def test_default_map_options(self):
        """
            Testing the widget map options from the project settings file
        """
        with override_settings(MAP_WIDGETS=MAP_WIDGETS):
            widget = GooglePointFieldWidget()
            self.assertEqual(hasattr(widget, "settings"), True)
            self.assertEqual(hasattr(widget, "settings_namespace"), True)
            options_str = widget.map_options()
            options = json.loads(options_str)
            self.assertEqual(options.get("zoom"), DEFAULT_GOOGLE_POINT_MAP_ZOOM)

