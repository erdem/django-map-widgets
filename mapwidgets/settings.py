from collections import defaultdict

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
            "readonly": {
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
            "interactive": {
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
            },
        }
    },
    "OSM": {
        "PointFieldWidget": {
            "interactive": {
                "zoom": 12,
                "markerFitZoom": 14,
                "showZoomNavigation": True,
                "mapCenterLocation": TIMEZONE_COORDINATES.get(getattr(django_settings, "TIME_ZONE", "UTC")),
            }
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

        self._app_settings = app_settings if app_settings is not None else self.django_settings
        self.defaults = defaults if defaults is not None else DEFAULTS

        self.merged = {**self.defaults, **self._app_settings}

    def __getattr__(self, attr):
        if attr not in self.merged:
            raise AttributeError(f"Invalid settings key: '{attr}'. Please check the settings documentation.")

        value = self.merged[attr]

        if isinstance(value, dict):
            value = MapWidgetSettings(value)
            self.merged[attr] = value  # cache the result

        return value

mw_settings = MapWidgetSettings(None, DEFAULTS)


def reload_widget_settings(*args, **kwargs):
    global mw_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == 'MAP_WIDGETS' and value:
        mw_settings = MapWidgetSettings(None, DEFAULTS)


setting_changed.connect(reload_widget_settings)
