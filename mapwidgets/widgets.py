import json

from django import forms
from django.contrib.gis.forms import BaseGeometryWidget
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils.http import urlencode

from mapwidgets.constants import STATIC_MAP_PLACEHOLDER_IMAGE
from mapwidgets.settings import MapWidgetSettings, mw_settings


def minify_if_not_debug(asset):
    """
        Transform template string `asset` by inserting '.min' if DEBUG=False
    """
    return asset.format('' if not mw_settings.MINIFED else '.min')


class BasePointFieldMapWidget(BaseGeometryWidget):
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
        return self.settings.merged

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


class GooglePointFieldWidget(BasePointFieldMapWidget):
    template_name = 'mapwidgets/google-point-field-widget.html'
    settings = mw_settings.GoogleMap.PointFieldWidget.interactive
    settings_namespace = 'mw_settings.GoogleMap.PointFieldWidget.interactive'

    @property
    def media(self):
        return self.generate_media(
            js_sources=[
                f"https://maps.googleapis.com/maps/api/js?libraries={mw_settings.LIBRARIES}&language={mw_settings.LANGUAGE}&key={mw_settings.GOOGLE_MAP_API_KEY}"
            ],
            css_files=[
                'mapwidgets/css/map_widgets{}.css',
            ],
            min_js='mapwidgets/js/mw_google_point_field.min.js',
            dev_js=[
                'mapwidgets/js/jquery_init.js',
                'mapwidgets/js/jquery_class.js',
                'mapwidgets/js/django_mw_base.js',
                'mapwidgets/js/mw_google_point_field.js'
            ]
        )


class MapboxPointFieldWidget(BasePointFieldMapWidget):
    template_name = 'mapwidgets/mapbox-point-field-widget.html'
    settings = mw_settings.Mapbox.PointFieldWidget.interactive
    settings_namespace = 'mw_settings.Mapbox.PointFieldWidget.interactive'

    @property
    def media(self):
        return self.generate_media(
            js_sources=[
                "https://api.mapbox.com/mapbox-gl-js/v2.5.1/mapbox-gl.js",
                "https://unpkg.com/@mapbox/mapbox-sdk/umd/mapbox-sdk.min.js",
                "https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.7.2/mapbox-gl-geocoder.min.js"
            ],
            css_files=[
                'mapwidgets/css/map_widgets{}.css',
                "https://api.mapbox.com/mapbox-gl-js/v2.5.1/mapbox-gl.css",
                "https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.7.2/mapbox-gl-geocoder.css"
            ],
            min_js='mapwidgets/js/mw_mapbox_point_field.min.js',
            dev_js=[
                'mapwidgets/js/jquery_init.js',
                'mapwidgets/js/jquery_class.js',
                'mapwidgets/js/django_mw_base.js',
                'mapwidgets/js/mw_mapbox_point_field.js'
            ]
        )


class OSMPointFieldWidget(BasePointFieldMapWidget):
    template_name = 'mapwidgets/osm_point_field_widget.html'
    settings_namespace = 'mw_settings.OSM.PointFieldWidget.interactive'
    settings = mw_settings.OSM.PointFieldWidget.interactive

    @property
    def media(self):

        css = {
            'all': [
                'https://unpkg.com/leaflet@1.7.1/dist/leaflet.css',
                'mapwidgets/css/map_widgets.css',
            ]
        }
        js = [
            'https://unpkg.com/leaflet@1.7.1/dist/leaflet.js',
            'mapwidgets/js/jquery_init.js',
            'mapwidgets/js/jquery_class.js',
            'mapwidgets/js/django_mw_base.js',
            'mapwidgets/js/mw_osm_point_field.js',
        ]

        return forms.Media(js=js, css=css)


class PointFieldInlineWidgetMixin(object):

    def get_js_widget_data(self, name, element_id):
        map_elem_selector = '#%s-mw-wrap' % name
        map_elem_id = '%s-map-elem' % name
        google_auto_input_id = '%s-mw-google-address-input' % name
        location_input_id = '#%s' % element_id
        js_widget_params = {
            'wrapElemSelector': map_elem_selector,
            'mapElemID': map_elem_id,
            'googleAutoInputID': google_auto_input_id,
            'locationInputID': location_input_id
        }
        return js_widget_params

    def render(self, name, value, attrs=None, renderer=None):
        if not attrs:
            attrs = dict()

        element_id = attrs.get('id')
        is_formset_empty_form_template = '__prefix__' in name
        widget_data = self.get_js_widget_data(name, element_id)
        attrs.update({
            'js_widget_data': json.dumps(widget_data),
            'is_formset_empty_form_template': is_formset_empty_form_template
        })
        self.as_super = super(PointFieldInlineWidgetMixin, self)
        if renderer is not None:
            return self.as_super.render(name, value, attrs, renderer)
        else:
            return self.as_super.render(name, value, attrs)


class GooglePointFieldInlineWidget(PointFieldInlineWidgetMixin, GooglePointFieldWidget):
    template_name = 'mapwidgets/google-point-field-inline-widget.html'
    settings = mw_settings.GoogleMap.PointFieldWidget.interactive
    settings_namespace = 'mw_settings.GoogleMap.PointFieldWidget.interactive'

    @property
    def media(self):
        css = {
            'all': [
                minify_if_not_debug('mapwidgets/css/map_widgets{}.css'),
            ]
        }

        js = [
            "https://maps.googleapis.com/maps/api/js?libraries={}&language={}&key={}".format(
                mw_settings.LIBRARIES, mw_settings.LANGUAGE, mw_settings.GOOGLE_MAP_API_KEY
            )
        ]

        if not mw_settings.MINIFED:  # pragma: no cover
            js = js + [
                'mapwidgets/js/jquery_init.js',
                'mapwidgets/js/jquery_class.js',
                'mapwidgets/js/django_mw_base.js',
                'mapwidgets/js/mw_google_point_field.js',
                'mapwidgets/js/mw_google_point_field_generater.js'
            ]
        else:
            js = js + [
                'mapwidgets/js/mw_google_point_inline_field.min.js'
            ]

        return forms.Media(js=js, css=css)


class BaseStaticMapWidget(forms.Widget):
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


class GoogleStaticMapWidget(BaseStaticMapWidget):
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    settings = mw_settings.GoogleMap.PointFieldWidget
    template_name = "mapwidgets/google-static-map.html"

    def __init__(self, zoom=None, size=None, *args, **kwargs):
        self.zoom = zoom
        self.size = size
        super(GoogleStaticMapWidget, self).__init__(*args, **kwargs)

    @property
    def map_settings(self):
        self.settings["key"] = mw_settings.GOOGLE_MAP_API_KEY

        if mw_settings.GOOGLE_MAP_API_SIGNATURE:  # pragma: no cover
            self.settings["signature"] = mw_settings.GOOGLE_MAP_API_SIGNATURE

        if self.size:
            self.settings["size"] = self.size
            self.settings["zoom"] = self.zoom
        return self.settings

    @property
    def marker_settings(self):
        if not isinstance(mw_settings.GoogleStaticMapMarkerSettings, dict):  # pragma: no cover
            raise TypeError('GoogleStaticMapMarkerSettings must be a dictionary.')

        return mw_settings.GoogleStaticMapMarkerSettings

    def get_point_field_params(self, latitude, longitude):
        marker_point = "%s,%s" % (latitude, longitude)

        marker_params = ["%s:%s" % (key, value) for key, value in self.marker_settings.items()]
        marker_params.append(marker_point)
        marker_url_params = "|".join(marker_params)
        params = {
            "center": marker_point,
            "markers": marker_url_params,
        }
        params.update(self.map_settings)
        return params

    def get_image_url(self, value):
        if isinstance(value, Point):
            longitude, latitude = value.x, value.y
            params = self.get_point_field_params(latitude, longitude)

            image_url_template = "%(base_url)s?%(params)s"
            image_url_data = {
                "base_url": self.base_url,
                "params": urlencode(params)
            }
            return image_url_template % image_url_data

        return static(STATIC_MAP_PLACEHOLDER_IMAGE)


class GoogleStaticOverlayMapWidget(GoogleStaticMapWidget):
    settings = mw_settings.GoogleMap.PointFieldWidget
    template_name = "mapwidgets/google-static-overlay-map.html"

    class Media:
        css = {
            "all": (
                minify_if_not_debug("mapwidgets/css/magnific-popup{}.css"),
            )
        }
        if not mw_settings.MINIFED:  # pragma: no cover
            js = (
                "mapwidgets/js/jquery_init.js",
                "mapwidgets/js/jquery.custom.magnific-popup.js",
            )
        else:
            js = (
                "mapwidgets/js/jquery.custom.magnific-popup.min.js",
            )

    def __init__(self, zoom=None, size=None, thumbnail_size=None, *args, **kwargs):
        self.thumbnail_size = thumbnail_size
        super(GoogleStaticOverlayMapWidget, self).__init__(zoom, size, *args, **kwargs)

    @property
    def map_settings(self):
        settings = super(GoogleStaticOverlayMapWidget, self).map_settings
        if self.thumbnail_size:
            settings["thumbnail_size"] = self.thumbnail_size
        return settings

    def get_thumbnail_url(self, value):
        if isinstance(value, Point):
            longitude, latitude = value.x, value.y
            params = self.get_point_field_params(latitude, longitude)
            params["size"] = params["thumbnail_size"]
            image_url_template = "%(base_url)s?%(params)s"
            image_url_data = {
                "base_url": self.base_url,
                "params": urlencode(params)
            }
            return image_url_template % image_url_data

        return static(STATIC_MAP_PLACEHOLDER_IMAGE)

    def get_context_data(self, name, value, attrs):
        context = super(GoogleStaticOverlayMapWidget, self).get_context_data(name, value, attrs)
        context["thumbnail_url"] = self.get_thumbnail_url(value)
        return context
