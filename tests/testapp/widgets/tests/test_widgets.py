import json

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings
from django.contrib.gis.geos import Point

from selenium import webdriver

from mapwidgets import GooglePointFieldWidget


DEFAULT_GOOGLE_POINT_MAP_CENTER_LOCATION = (51.5073509, -0.12775829999)
DEFAULT_GOOGLE_POINT_MAP_ZOOM = 15
GOOGLE_MAP_API_KEY = "AIzaSyC6BeCYCBSWDdC3snYRFKWw18bd9MA-uu4"


class GooglePointWidgetUnitTests(TestCase):

    def test_widget_with_default_settings(self):
        """
            Testing the widget map options from the project settings file
        """

        widget_settings = {
            "GooglePointFieldWidget": (
                ("zoom", DEFAULT_GOOGLE_POINT_MAP_ZOOM),
                ("mapCenterLocation", DEFAULT_GOOGLE_POINT_MAP_CENTER_LOCATION),
            )
        }

        with override_settings(MAP_WIDGETS=widget_settings):
            widget = GooglePointFieldWidget()
            self.assertEqual(hasattr(widget, "settings"), True)
            self.assertEqual(hasattr(widget, "settings_namespace"), True)
            options_str = widget.map_options()
            options = json.loads(options_str)
            self.assertEqual(options.get("zoom"), DEFAULT_GOOGLE_POINT_MAP_ZOOM)

            point = Point(-104.9903, 39.7392)

            default_attrs = {
                'required': True,
                'id': 'id_location'
            }
            result = widget.render(name="location", value=point, attrs=default_attrs)
            self.assertIn(widget.serialize(point), result)


