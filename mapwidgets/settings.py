from django.conf import settings as django_settings
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
    "Leaflet": {
        "PointFieldWidget": {
            "interactive": {
                "mapOptions": {
                    "zoom": 12,
                    "scrollWheelZoom": False
                },
                "tileLayer": {
                    "urlTemplate": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                    "options": {
                        "maxZoom": 20
                    }
                },
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
    def __init__(self, defaults=None, app_settings=None):
        self.django_settings = getattr(django_settings, 'MAP_WIDGETS', {})
        self._app_settings = app_settings if app_settings is not None else self.django_settings
        self.defaults = defaults if defaults is not None else DEFAULTS
        self._merged = self.merge_dict(self.defaults, self._app_settings)

    def dict(self):
        return self._merged

    @classmethod
    def merge_dict(cls, dict1, dict2):
        for key, val in dict1.items():
            if isinstance(val, dict):
                if key in dict2 and type(dict2[key] == dict):
                    cls.merge_dict(dict1[key], dict2[key])
            else:
                if key in dict2:
                    dict1[key] = dict2[key]

        for key, val in dict2.items():
            if key not in dict1:
                dict1[key] = val
        return dict1

    def __getattr__(self, attr):
        if attr not in self._merged:
            raise AttributeError(f"Invalid settings key: '{attr}'")
        value = self._merged[attr]
        if isinstance(value, dict):
            value = MapWidgetSettings(value)
            self._merged[attr] = value
        return value


mw_settings = MapWidgetSettings(DEFAULTS)


def reload_widget_settings(*args, **kwargs):
    global mw_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == 'MAP_WIDGETS' and value:
        mw_settings = MapWidgetSettings(value, DEFAULTS)


setting_changed.connect(reload_widget_settings)
