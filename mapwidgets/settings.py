from collections import OrderedDict

from django.conf import settings as django_settings
from django.utils.functional import cached_property

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
    "MINIFED": not django_settings.DEBUG,
    "GOOGLE_MAP_API_SIGNATURE": "",
    "GOOGLE_MAP_API_KEY": "",
}


class MapWidgetSettings(object):

    def __init__(self, user_settings=None, defaults=None):
        if user_settings:
            self._user_settings = user_settings

        self.defaults = defaults or DEFAULTS

    @cached_property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(django_settings, 'MAP_WIDGETS', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid Django Map Widgets setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]

            # Merge user multi value settings with defaults
            if isinstance(val, tuple):
                try:
                    user_bundle = OrderedDict(val)
                    default_bundle = OrderedDict(self.defaults[attr])
                    default_bundle.update(user_bundle)
                    val = default_bundle
                except TypeError:
                    pass

        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]
            if isinstance(val, tuple):
                try:
                    val = OrderedDict(val)
                except TypeError:
                    pass


        # Cache the result
        setattr(self, attr, val)
        return val

mw_settings = MapWidgetSettings()
