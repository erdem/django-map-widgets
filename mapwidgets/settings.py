from collections import OrderedDict

from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _
from django.test.signals import setting_changed

from mapwidgets.constants import TIMEZONE_COORDINATES


DEFAULTS = {
    "GooglePointFieldWidget": (
        ("mapCenterLocationName", None),
        ("mapCenterLocation", TIMEZONE_COORDINATES.get(getattr(django_settings, "TIME_ZONE", "UTC"))),
        ("zoom", 6),
        ("GooglePlaceAutocompleteOptions", {}),
        ("markerFitZoom", 15),
    ),

    "GoogleStaticMapWidget": (
        ("zoom", 15),
        ("size", "480x480"),
        ("scale", ""),
        ("format", ""),
        ("maptype", ""),
        ("path", ""),
        ("visible", ""),
        ("style", ""),
        ("language", ""),
        ("region", "")
    ),

    "GoogleStaticMapMarkerSettings": (
        ("size", "normal"),
        ("color", ""),
        ("icon", ""),
    ),

    "GoogleStaticOverlayMapWidget": (
        ("zoom", 15),
        ("size", "480x480"),
        ("thumbnail_size", "160x160"),
        ("scale", ""),
        ("format", ""),
        ("maptype", ""),
        ("path", ""),
        ("visible", ""),
        ("style", ""),
        ("language", ""),
        ("region", "")
    ),
    "LANGUAGE": "en",
    "MINIFED": not django_settings.DEBUG,
    "GOOGLE_MAP_API_SIGNATURE": "",
    "GOOGLE_MAP_API_KEY": "",
}


class MapWidgetSettings(object):

    def __init__(self, app_settings=None, defaults=None):
        if app_settings:
            if not isinstance(app_settings, (dict, tuple)):
                raise TypeError(_("MapWidget settings must be a tuple or dictionary"))
            self._app_settings = app_settings

        self.defaults = defaults or DEFAULTS

    @property
    def app_settings(self):
        if not hasattr(self, '_app_settings'):
            app_settings = getattr(django_settings, 'MAP_WIDGETS', {})
            if not isinstance(app_settings, (dict, tuple)):
                raise TypeError(_("MapWidget settings must be a tuple or dictionary"))

            self._app_settings = getattr(django_settings, 'MAP_WIDGETS', {})
        return self._app_settings

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid settings key: '%s'. Please check the settings documentation http://django-map-widgets.readthedocs.io/en/latest/widgets/settings.html" % attr)

        try:
            # Check if present attr in user settings
            val = self.app_settings[attr]

            # Merge app tuple settings with defaults
            if isinstance(val, tuple):
                try:
                    app_bundle = OrderedDict(val)
                    default_bundle = OrderedDict(self.defaults[attr])
                    default_bundle.update(app_bundle)
                    val = default_bundle
                except ValueError:
                    raise ValueError(_("Invalid %s settings value. Please check the settings documentation http://django-map-widgets.readthedocs.io/en/latest/widgets/settings.html" % attr))

            # Merge app dict settings with defaults
            if isinstance(val, dict):
                default_bundle = OrderedDict(self.defaults[attr])
                default_bundle.update(val)
                val = default_bundle

        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]
            if isinstance(val, tuple):
                try:
                    val = OrderedDict(val)
                except ValueError:
                    raise ValueError(_("Invalid %s settings value. Please check the settings documentation http://django-map-widgets.readthedocs.io/en/latest/widgets/settings.html" % attr))

        # Cache the result
        setattr(self, attr, val)
        return val

mw_settings = MapWidgetSettings(None, DEFAULTS)


def reload_widget_settings(*args, **kwargs):
    global mw_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == 'MAP_WIDGETS' and value:
        mw_settings = MapWidgetSettings(None, DEFAULTS)

setting_changed.connect(reload_widget_settings)
