import json

from django.test import TestCase
from django.test.utils import override_settings
from django.utils.six.moves import reload_module
from django.contrib.gis.geos import Point
from django.utils.html import escapejs

from mapwidgets import widgets as mw_widgets


class GooglePointWidgetUnitTests(TestCase):

    def test_widget_with_default_settings(self):
        """
            Test the widget with default map options in the django project settings file
        """
        zoom = 15
        default_map_center = [51.5073509, -0.12775829999]
        widget_settings = {
            "GooglePointFieldWidget": (
                ("zoom", zoom),
                ("mapCenterLocation", default_map_center),
            )
        }

        with override_settings(MAP_WIDGETS=widget_settings):
            reload_module(mw_widgets)
            widget = mw_widgets.GooglePointFieldWidget()
            self.assertEqual(hasattr(widget, "settings"), True)
            self.assertEqual(hasattr(widget, "settings_namespace"), True)

            # test `map_options` method
            options_str = widget.map_options()
            options = json.loads(options_str)
            self.assertEqual(options.get("zoom"), zoom)
            self.assertEqual(options.get("mapCenterLocation"), default_map_center)

            # test render
            point = Point(-104.9903, 39.7392)
            widget_html_elem_id = "id_location"
            widget_html_elem_name = "location"
            result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
            self.assertIn(widget.serialize(point), result)
            self.assertIn(widget_html_elem_id, result)
            self.assertIn(escapejs(options_str), result)

    def test_widget_with_custom_settings(self):
        zoom = 11
        default_map_center = [52.5073509, -0.23775829999]
        widget_settings = {
            "GooglePointFieldWidget": (
                ("zoom", zoom),
                ("mapCenterLocation", default_map_center),
            )
        }

        widget = mw_widgets.GooglePointFieldWidget(settings=widget_settings)
        self.assertEqual(hasattr(widget, "settings"), True)
        self.assertEqual(hasattr(widget, "settings_namespace"), True)

        # test `map_options` method
        options_str = widget.map_options()
        options = json.loads(options_str)
        self.assertEqual(options.get("zoom"), zoom)
        self.assertEqual(options.get("mapCenterLocation"), default_map_center)

        # test render
        point = Point(-105.9903, 38.7392)
        widget_html_elem_id = "id_location"
        widget_html_elem_name = "location"
        result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
        self.assertIn(widget.serialize(point), result)
        self.assertIn(widget_html_elem_id, result)
        self.assertIn(escapejs(options_str), result)


class GooglePointInlineWidgetUnitTests(TestCase):
    def test_widget_with_default_settings(self):
        """
            Test the widget with default map options in the django project settings file
        """
        zoom = 15
        default_map_center = [51.5073509, -0.12775829999]
        widget_settings = {
            "GooglePointFieldWidget": (
                ("zoom", zoom),
                ("mapCenterLocation", default_map_center),
            )
        }

        with override_settings(MAP_WIDGETS=widget_settings):
            reload_module(mw_widgets)
            widget = mw_widgets.GooglePointFieldInlineWidget()
            self.assertEqual(hasattr(widget, "settings"), True)
            self.assertEqual(hasattr(widget, "settings_namespace"), True)

            # test `map_options` method
            options_str = widget.map_options()
            options = json.loads(options_str)
            self.assertEqual(options.get("zoom"), zoom)
            self.assertEqual(options.get("mapCenterLocation"), default_map_center)

            # test render
            point = Point(-104.9903, 39.7392)
            widget_html_elem_id = "id_location"
            widget_html_elem_name = "location"
            result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
            self.assertIn(widget.serialize(point), result)
            self.assertIn(widget_html_elem_id, result)

            # test widget as a formset empty form
            widget_html_elem_id = "__prefix__id_location"
            result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
            self.assertIn(widget.serialize(point), result)
            inline_widget_data = widget.get_js_widget_data(widget_html_elem_name, widget_html_elem_id)
            self.assertIn(escapejs(json.dumps(inline_widget_data)), result)

    def test_widget_with_custom_settings(self):
        zoom = 11
        default_map_center = [52.5073509, -0.23775829999]
        widget_settings = {
            "GooglePointFieldWidget": (
                ("zoom", zoom),
                ("mapCenterLocation", default_map_center),
            )
        }

        widget = mw_widgets.GooglePointFieldInlineWidget(settings=widget_settings)
        self.assertEqual(hasattr(widget, "settings"), True)
        self.assertEqual(hasattr(widget, "settings_namespace"), True)

        # test `map_options` method
        options_str = widget.map_options()
        options = json.loads(options_str)
        self.assertEqual(options.get("zoom"), zoom)
        self.assertEqual(options.get("mapCenterLocation"), default_map_center)

        # test render
        point = Point(-105.9903, 38.7392)
        widget_html_elem_id = "id_location"
        widget_html_elem_name = "location"
        result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
        self.assertIn(widget.serialize(point), result)
        self.assertIn(widget_html_elem_id, result)

        # test widget as a formset empty form
        widget_html_elem_id = "__prefix__id_location"
        result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
        self.assertIn(widget.serialize(point), result)
        inline_widget_data = widget.get_js_widget_data(widget_html_elem_name, widget_html_elem_id)
        self.assertIn(escapejs(json.dumps(inline_widget_data)), result)
