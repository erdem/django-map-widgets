from django.conf import settings as django_settings
from django.utils.translation import gettext_lazy as _
from django.test.signals import setting_changed

from mapwidgets.constants import TIMEZONE_COORDINATES


DEFAULTS = {
    "GoogleMap": {
        "PointFieldWidget": {
            "interactive": {
                "mapCenterLocationName": None,
                "mapCenterLocation": TIMEZONE_COORDINATES.get(getattr(django_settings, "TIME_ZONE", "UTC")),
                "zoom": 12,
                "scrollWheel": False,
                "GooglePlaceAutocompleteOptions": {},
                "markerFitZoom": 14,
                "streetViewControl": True,
            },
            "read-only": {
                "thumbnail": {
                    "zoom": 15,
                    "size": "480x480",
                    "scale": "",
                    "format": "",
                    "maptype": "",
                    "path": "",
                    "visible": "",
                    "style": "",
                    "language": "",
                    "region": "",
                    "marker": {
                        "size": "normal",
                        "color": "",
                        "icon": "",
                    }
                },
                "overlay": {
                    "zoom": 15,
                    "size": "480x480",
                    "thumbnail_size": "160x160",
                    "scale": "",
                    "format": "",
                    "maptype": "",
                    "path": "",
                    "visible": "",
                    "style": "",
                    "language": "",
                    "region": "",
                    "marker": {
                        "size": "normal",
                        "color": "",
                        "icon": "",
                    }
                },
            }
        }
    },
    "Mapbox": {
        "PointFieldWidget": {
            "access_token": "",
            "markerFitZoom": 14,
            "showZoomNavigation": True,
            "mapOptions": {
                "zoom": 12,
                "style": "mapbox://styles/mapbox/streets-v11",
                "scrollZoom": False,
                "animate": False,
                "center": TIMEZONE_COORDINATES.get(getattr(django_settings, "TIME_ZONE", "UTC")),
            },
            "geocoderOptions": {
                "zoom": 6,
                "flyTo": False,
                "style": "mapbox://styles/mapbox/streets-v11",
                "reverseGeocode": True,
                "marker": False,
            }
        }
    },
    "OpenStreetMap": {
        "PointFieldWidget": {
            "zoom": 12,
            "markerFitZoom": 14,
            "showZoomNavigation": True,
            "mapCenterLocation": TIMEZONE_COORDINATES.get(getattr(django_settings, "TIME_ZONE", "UTC")),
        }
    },
    "LANGUAGE": "en",
    "LIBRARIES": "places",
    "srid": 4326,
    "MINIFED": not django_settings.DEBUG,
    "GOOGLE_MAP_API_SIGNATURE": "",
    "GOOGLE_MAP_API_KEY": "",
    "MAPBOX_API_KEY": "",
}


class MapWidgetSettings:
    def __init__(self, app_settings=None, defaults=None):
        self.django_settings = getattr(django_settings, 'MAP_WIDGETS', {})

        self._app_settings = app_settings if isinstance(app_settings, dict) else self.django_settings
        self.defaults = defaults or DEFAULTS

    @property
    def app_settings(self):
        return self._app_settings

    def get_settings(self, attr):
        user_settings = self.app_settings.get(attr, {})
        default_settings = self.defaults.get(attr, {})

        if not user_settings:
            return default_settings

        # Merge settings, with user settings overriding defaults
        try:
            merged_settings = {**default_settings, **user_settings}
        except TypeError:
            raise TypeError(f"Invalid settings type: '{attr}'. Please check the settings documentation.")
        return merged_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(f"Invalid settings key: '{attr}'. Please check the settings documentation.")

        settings = self.get_settings(attr)
        setattr(self, attr, settings)  # Cache the result
        return settings


mw_settings = MapWidgetSettings(None, DEFAULTS)


def reload_widget_settings(*args, **kwargs):
    global mw_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == 'MAP_WIDGETS' and value:
        mw_settings = MapWidgetSettings(None, DEFAULTS)


setting_changed.connect(reload_widget_settings)
