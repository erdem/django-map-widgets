from collections import OrderedDict

from django.test import TestCase
from django.test.utils import override_settings
from django.utils.six.moves import reload_module

from mapwidgets.settings import MapWidgetSettings, DEFAULTS


class WidgetSettingsTests(TestCase):
    def test_default_settings_values(self):
        mw_settings = MapWidgetSettings()

        google_point_widget_default_settings = OrderedDict(DEFAULTS["GooglePointFieldWidget"])
        self.assertEqual(mw_settings.GooglePointFieldWidget, google_point_widget_default_settings)

        google_static_widget_default_settings = OrderedDict(DEFAULTS["GoogleStaticMapWidget"])
        self.assertEqual(mw_settings.GoogleStaticMapWidget, google_static_widget_default_settings)

        google_static_widget_marker_default_settings = OrderedDict(DEFAULTS["GoogleStaticMapMarkerSettings"])
        self.assertEqual(mw_settings.GoogleStaticMapMarkerSettings, google_static_widget_marker_default_settings)

        google_static_overlay_widget_default_settings = OrderedDict(DEFAULTS["GoogleStaticOverlayMapWidget"])
        self.assertEqual(mw_settings.GoogleStaticOverlayMapWidget, google_static_overlay_widget_default_settings)

    def test_custom_settings_values(self):
        zoom = 11
        map_center = [34.5073509, -30.12775829]
        static_map_size = "320x320"

        custom_settings = {
            "GooglePointFieldWidget": (
                ("zoom", zoom),
                ("mapCenterLocation", map_center),
            ),
            "GoogleStaticMapWidget": (
                ("zoom", zoom),
                ("size", static_map_size),
            )
        }

        with override_settings(MAP_WIDGETS=custom_settings):
            mw_settings = MapWidgetSettings()

            google_point_widget_settings = mw_settings.GooglePointFieldWidget
            self.assertEqual(google_point_widget_settings.get("zoom"), zoom)
            self.assertEqual(google_point_widget_settings.get("mapCenterLocation"), map_center)

            google_point_static_widget_settings = mw_settings.GoogleStaticMapWidget
            self.assertEqual(google_point_static_widget_settings.get("zoom"), zoom)
            self.assertEqual(google_point_static_widget_settings.get("size"), static_map_size)

    def test_settings_validations(self):
        with override_settings(MAP_WIDGETS="invalid_map_widgets_settings_type"):
            self.assertRaises(TypeError, lambda: getattr(MapWidgetSettings(), "GooglePointFieldWidget"))

        invalid_tuple_settings = {
            "GooglePointFieldWidget": (
                ("zoom", 12, "invalid_value"),
            ),
        }

        with override_settings(MAP_WIDGETS=invalid_tuple_settings):
            self.assertRaises(ValueError, lambda: getattr(MapWidgetSettings(), "GooglePointFieldWidget"))

        # test custom settings parameter validations
        self.assertRaises(TypeError, lambda: MapWidgetSettings(app_settings=1))

        # test defaults parameter with invalid value
        self.assertRaises(ValueError, lambda: getattr(MapWidgetSettings(defaults=invalid_tuple_settings), "GooglePointFieldWidget"))