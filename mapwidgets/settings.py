from django.conf import settings as django_settings
from django.utils.translation import gettext_lazy as _
from django.test.signals import setting_changed

from mapwidgets.constants import TIMEZONE_COORDINATES


DEFAULTS = {
    "GooglePointFieldWidget": (
        ("mapCenterLocationName", None),
        ("mapCenterLocation", TIMEZONE_COORDINATES.get(getattr(django_settings, "TIME_ZONE", "UTC"))),
        ("zoom", 12),
        ("scrollWheel", False),
        ("GooglePlaceAutocompleteOptions", {}),
        ("markerFitZoom", 14),
        ("streetViewControl", True),
    ),

    "MapboxPointFieldWidget": (
        ("access_token", ""),
        ("markerFitZoom", 14),
        ("showZoomNavigation", True),
        ("mapOptions", {
            "zoom": 12,
            "style": "mapbox://styles/mapbox/streets-v11",
            "scrollZoom": False,
            "animate": False,
            "center": TIMEZONE_COORDINATES.get(getattr(django_settings, "TIME_ZONE", "UTC")),
        }),
        ("geocoderOptions", {
            "zoom": 6,
            "flyTo": False,
            "style": "mapbox://styles/mapbox/streets-v11",
            "reverseGeocode": True,
            "marker": False,
        })
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
    "LIBRARIES": "places",
    "srid": 4326,
    "MINIFED": not django_settings.DEBUG,
    "GOOGLE_MAP_API_SIGNATURE": "",
    "GOOGLE_MAP_API_KEY": "",
    "MAPBOX_API_KEY": "",
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
            settings = self.app_settings[attr]

            # Merge app tuple settings with defaults
            if isinstance(settings, tuple):
                try:
                    # support backwards compatibility for old settings format
                    settings = dict(settings)
                except ValueError:
                    raise ValueError(_("Invalid %s settings value. Please check the settings documentation http://django-map-widgets.readthedocs.io/en/latest/widgets/settings.html" % attr))

            # Merge app dict settings with defaults
            if type(settings) is dict:
                django_settings = dict(self.defaults[attr])
                for key, value in settings.items():
                    # merge nested settings with defaults if it is dictionary
                    if type(value) is dict:
                        nested_setting = django_settings[key]
                        for k, v in value.items():
                            nested_setting[k] = v
                        value = nested_setting
                    django_settings[key] = value
                settings = django_settings

        except KeyError:
            # Fall back to defaults
            settings = self.defaults[attr]
            if isinstance(settings, tuple):
                try:
                    settings = dict(settings)
                except ValueError:
                    raise ValueError(_("Invalid %s settings value. Please check the settings documentation http://django-map-widgets.readthedocs.io/en/latest/widgets/settings.html" % attr))

        # Cache the result
        setattr(self, attr, settings)
        return settings


mw_settings = MapWidgetSettings(None, DEFAULTS)


def reload_widget_settings(*args, **kwargs):
    global mw_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == 'MAP_WIDGETS' and value:
        mw_settings = MapWidgetSettings(None, DEFAULTS)


setting_changed.connect(reload_widget_settings)
