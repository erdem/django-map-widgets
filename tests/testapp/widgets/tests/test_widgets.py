import os
import json

try:
    from urllib.request import urlopen
    from http.client import HTTPMessage
except ImportError:
    from urllib import urlopen

from django.test import TestCase
from django.test.utils import override_settings
from django.utils.six.moves import reload_module
from django.contrib.gis.geos import Point
from django.utils.html import escapejs
from django.conf import settings as test_app_settings
from django import forms as django_forms

from mapwidgets import widgets as mw_widgets

from .utils import html_escape, get_textarea_html

GOOGLE_MAP_API_KEY = os.environ.get("TEST_GOOGLE_MAP_API_KEY", test_app_settings.GOOGLE_MAP_API_KEY)

DJANGO_DEFAULT_SRID_VALUE = 4326
GOOGLE_MAP_DEFAULT_SRID_VALUE = 4326


class GooglePointWidgetUnitTests(TestCase):

    def test_widget_with_default_settings(self):
        """
            Test the widget with default settings which is defined in django settings file
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
            self.assertEqual(isinstance(widget.media, django_forms.Media), True)

            # test `map_options` method
            options_str = widget.map_options()
            options = json.loads(options_str)
            self.assertEqual(options.get("zoom"), zoom)
            self.assertEqual(options.get("mapCenterLocation"), default_map_center)

            # test render with Point object value
            point = Point(-104.9903, 39.7392, srid=DJANGO_DEFAULT_SRID_VALUE)
            widget_html_elem_id = "id_location"
            widget_html_elem_name = "location"
            result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
            self.assertIn(widget.serialize(point), result)
            self.assertIn(get_textarea_html(widget_html_elem_id, widget_html_elem_name, point), result)
            self.assertIn(escapejs(options_str), result)

            # test render with serialized data value
            result = widget.render(name=widget_html_elem_name, value=widget.serialize(point))
            self.assertIn(widget.serialize(point), result)

            # test widget `attrs` param
            w = mw_widgets.GooglePointFieldWidget(attrs={"max-height": 600})
            self.assertIn("max-height", w.attrs)

            # test widget render `attrs` param with `None` value
            self.assertIn(widget_html_elem_name, w.render(name=widget_html_elem_name, value=None, attrs=None))

    def test_widget_with_custom_settings(self):
        """
            Test the widget with custom settings which is updated by `settings` parameter
        """
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
        self.assertEqual(isinstance(widget.media, django_forms.Media), True)

        # test `map_options` method
        options_str = widget.map_options()
        options = json.loads(options_str)
        self.assertEqual(options.get("zoom"), zoom)
        self.assertEqual(options.get("mapCenterLocation"), default_map_center)

        # test render with Point object value
        point = Point(-105.9903, 38.73922, srid=DJANGO_DEFAULT_SRID_VALUE)
        widget_html_elem_id = "id_location"
        widget_html_elem_name = "location"
        result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
        self.assertIn(widget.serialize(point), result)
        self.assertIn(get_textarea_html(widget_html_elem_id, widget_html_elem_name, point), result)
        self.assertIn(escapejs(options_str), result)

        # test render with serialized data value
        result = widget.render(name=widget_html_elem_name, value=widget.serialize(point))
        self.assertIn(widget.serialize(point), result)

    def test_widget_with_different_srid(self):
        """
            Test the widget with a different `srid` value instead of Geo Django default
        """
        point = Point(-16351.8201902, 6708983.38973, srid=3857)
        widget_html_elem_id = "id_location"
        widget_html_elem_name = "location"
        widget = mw_widgets.GooglePointFieldWidget(map_srid=3857)
        result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})

        ogr = point.ogr
        ogr.transform(GOOGLE_MAP_DEFAULT_SRID_VALUE)
        point_with_google_map_srid_format = ogr
        self.assertIn(widget.serialize(point_with_google_map_srid_format), result)


class GooglePointInlineWidgetUnitTests(TestCase):

    def test_widget_with_default_settings(self):
        """
            Test widget with default settings which is defined in django settings file
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
            self.assertEqual(isinstance(widget.media, django_forms.Media), True)

            # test `map_options` method
            options_str = widget.map_options()
            options = json.loads(options_str)
            self.assertEqual(options.get("zoom"), zoom)
            self.assertEqual(options.get("mapCenterLocation"), default_map_center)

            # test render with Point object value
            point = Point(-104.9903, 39.73922, srid=DJANGO_DEFAULT_SRID_VALUE)
            widget_html_elem_id = "id_location"
            widget_html_elem_name = "location"
            result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
            self.assertIn(widget.serialize(point), result)
            self.assertIn(get_textarea_html(widget_html_elem_id, widget_html_elem_name, point), result)

            # test render with serialized data value
            result = widget.render(name=widget_html_elem_name, value=widget.serialize(point))
            self.assertIn(widget.serialize(point), result)

            # test widget as a formset empty form
            result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
            self.assertIn(widget.serialize(point), result)
            inline_widget_data = widget.get_js_widget_data(widget_html_elem_name, widget_html_elem_id)
            self.assertIn(escapejs(json.dumps(inline_widget_data)), result)

            # test widget `attrs` param
            w = mw_widgets.GooglePointFieldInlineWidget(attrs={"max-height": 600})
            self.assertIn("max-height", w.attrs)

            # test widget render `attrs` param with `None` value
            self.assertIn(widget_html_elem_name, w.render(name=widget_html_elem_name, value=None, attrs=None))

    def test_widget_with_custom_settings(self):
        """
            Test the widget with custom settings which is updated by `settings` parameter
        """
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
        self.assertEqual(isinstance(widget.media, django_forms.Media), True)

        # test `map_options` method
        options_str = widget.map_options()
        options = json.loads(options_str)
        self.assertEqual(options.get("zoom"), zoom)
        self.assertEqual(options.get("mapCenterLocation"), default_map_center)

        # test render with Point object value
        point = Point(-105.9903, 38.73922, srid=DJANGO_DEFAULT_SRID_VALUE)
        widget_html_elem_id = "id_location"
        widget_html_elem_name = "location"
        result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
        self.assertIn(widget.serialize(point), result)
        self.assertIn(get_textarea_html(widget_html_elem_id, widget_html_elem_name, point), result)

        # test render with serialized data value
        result = widget.render(name=widget_html_elem_name, value=widget.serialize(point))
        self.assertIn(widget.serialize(point), result)

        # test widget as a formset empty form
        widget_html_elem_id = "__prefix__id_location"
        result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
        self.assertIn(widget.serialize(point), result)
        inline_widget_data = widget.get_js_widget_data(widget_html_elem_name, widget_html_elem_id)
        self.assertIn(escapejs(json.dumps(inline_widget_data)), result)


class GoogleStaticMapWidgetUnitTests(TestCase):

    def test_widget_with_default_settings(self):
        """
            Test the widget with default settings which is defined in django settings file
        """
        zoom = 13
        map_size = "200x200"
        widget_settings = {
            "GoogleStaticMapWidget": (
                ("zoom", zoom),
                ("size", map_size),
            ),
            "GOOGLE_MAP_API_KEY": GOOGLE_MAP_API_KEY,
        }

        with override_settings(MAP_WIDGETS=widget_settings):
            reload_module(mw_widgets)
            widget = mw_widgets.GoogleStaticMapWidget()
            settings = widget.map_settings

            # test `map_settings` method
            self.assertEqual(settings.get("zoom"), zoom)
            self.assertEqual(settings.get("size"), map_size)

            # test render
            point = Point(-105.9903, 38.7392)
            widget_html_elem_id = "id_location"
            widget_html_elem_name = "location"
            result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
            map_image_url = widget.get_image_url(point)
            self.assertIn(GOOGLE_MAP_API_KEY, map_image_url)
            self.assertIn(html_escape(map_image_url), result)

            # test map_image_url
            res = urlopen(map_image_url)
            self.assertEqual(res.getcode(), 200)
            if hasattr(res.info(), 'type'):
                self.assertEqual(res.info().type, "image/png")
            else:
                self.assertEqual(res.info().get_content_type(), "image/png")

            # test map_image_url with `None` value
            result = widget.render(name=widget_html_elem_name, value=None, attrs={'id': widget_html_elem_id})
            map_image_url = widget.get_image_url(None)
            self.assertIn(map_image_url, result)

    def test_widget_with_custom_settings(self):
        """
            Test the widget with custom settings which is updated by `settings` parameter
        """
        zoom = 9
        map_size = "100x100"

        widget_settings = {
            "GoogleStaticMapWidget": (
                ("zoom", zoom),
                ("size", map_size),
            ),
            "GOOGLE_MAP_API_KEY": GOOGLE_MAP_API_KEY,
        }

        with override_settings(MAP_WIDGETS=widget_settings):
            reload_module(mw_widgets)
            widget = mw_widgets.GoogleStaticMapWidget(zoom=zoom, size=map_size)
            settings = widget.map_settings

            # test `map_settings` method
            self.assertEqual(settings.get("zoom"), zoom)
            self.assertEqual(settings.get("size"), map_size)

            # test render
            point = Point(-105.9903, 38.7392)
            widget_html_elem_id = "id_location"
            widget_html_elem_name = "location"
            result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
            map_image_url = widget.get_image_url(point)
            self.assertIn(GOOGLE_MAP_API_KEY, map_image_url)
            self.assertIn(html_escape(map_image_url), result)

            # test map_image_url
            res = urlopen(map_image_url)
            self.assertEqual(res.getcode(), 200)
            if hasattr(res.info(), 'type'):
                self.assertEqual(res.info().type, "image/png")
            else:
                self.assertEqual(res.info().get_content_type(), "image/png")


class GoogleStaticOverlayMapWidgetUnitTests(TestCase):

    def test_widget_with_default_settings(self):
        """
            Test the widget with default settings which is defined in django settings file
        """
        zoom = 18
        map_size = "400x400"
        thumbnail_size = "100x100"
        widget_settings = {
            "GoogleStaticOverlayMapWidget": (
                ("zoom", zoom),
                ("size", map_size),
                ("thumbnail_size", thumbnail_size),
            ),
            "GOOGLE_MAP_API_KEY": GOOGLE_MAP_API_KEY,
        }

        with override_settings(MAP_WIDGETS=widget_settings):
            reload_module(mw_widgets)
            widget = mw_widgets.GoogleStaticOverlayMapWidget()
            settings = widget.map_settings

            # test `map_settings` method
            self.assertEqual(settings.get("zoom"), zoom)
            self.assertEqual(settings.get("size"), map_size)
            self.assertEqual(settings.get("thumbnail_size"), thumbnail_size)

            # test render
            point = Point(-92.9903, 34.7392)
            widget_html_elem_id = "id_location"
            widget_html_elem_name = "location"
            result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
            map_image_url = widget.get_image_url(point)
            self.assertIn(GOOGLE_MAP_API_KEY, map_image_url)
            self.assertIn(html_escape(map_image_url), result)

            # test map_image_url
            res = urlopen(map_image_url)
            self.assertEqual(res.getcode(), 200)
            if hasattr(res.info(), 'type'):
                self.assertEqual(res.info().type, "image/png")
            else:
                self.assertEqual(res.info().get_content_type(), "image/png")

            # test thumbnail_image_url
            thumbnail_url = widget.get_thumbnail_url(point)
            res = urlopen(thumbnail_url)
            self.assertEqual(res.getcode(), 200)
            if hasattr(res.info(), 'type'):
                self.assertEqual(res.info().type, "image/png")
            else:
                self.assertEqual(res.info().get_content_type(), "image/png")

            # test map_image_url with `None` value
            result = widget.render(name=widget_html_elem_name, value=None, attrs={'id': widget_html_elem_id})
            thumbnail_url = widget.get_thumbnail_url(None)
            self.assertIn(thumbnail_url, result)

    def test_widget_with_custom_settings(self):
        """
            Test the widget with custom settings which is updated by `settings` parameter
        """
        zoom = 18
        map_size = "300x300"
        thumbnail_size = "75x75"

        widget_settings = {
            "GOOGLE_MAP_API_KEY": GOOGLE_MAP_API_KEY,
        }

        with override_settings(MAP_WIDGETS=widget_settings):
            reload_module(mw_widgets)
            widget = mw_widgets.GoogleStaticOverlayMapWidget(zoom=zoom, size=map_size, thumbnail_size=thumbnail_size)
            settings = widget.map_settings

            # test `map_settings` method
            self.assertEqual(settings.get("zoom"), zoom)
            self.assertEqual(settings.get("size"), map_size)

            # test render
            point = Point(-105.9903, 38.7392)
            widget_html_elem_id = "id_location"
            widget_html_elem_name = "location"
            result = widget.render(name=widget_html_elem_name, value=point, attrs={'id': widget_html_elem_id})
            map_image_url = widget.get_image_url(point)
            self.assertIn(GOOGLE_MAP_API_KEY, map_image_url)
            self.assertIn(html_escape(map_image_url), result)

            # test map_image_url
            res = urlopen(map_image_url)
            self.assertEqual(res.getcode(), 200)
            if hasattr(res.info(), 'type'):
                self.assertEqual(res.info().type, "image/png")
            else:
                self.assertEqual(res.info().get_content_type(), "image/png")

            # test thumbnail_image_url
            thumbnail_url = widget.get_thumbnail_url(point)
            res = urlopen(thumbnail_url)
            self.assertEqual(res.getcode(), 200)
            if hasattr(res.info(), 'type'):
                self.assertEqual(res.info().type, "image/png")
            else:
                self.assertEqual(res.info().get_content_type(), "image/png")
