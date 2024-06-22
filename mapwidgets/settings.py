from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.test.signals import setting_changed

from mapwidgets.constants import TIMEZONE_COORDINATES


def get_default_center_coordinates():
    try:
        django_time_zone = django_settings.TIME_ZONE
    except ImproperlyConfigured:
        django_time_zone = "UTC"
    return TIMEZONE_COORDINATES.get(django_time_zone, None)


DEFAULT_SETTINGS = {
    "GoogleMap": {
        "apiKey": None,
        "apiSecret": None,
        "CDNURLParams": {
            "language": "en",
            "libraries": "places,marker",
            "loading": "async",
            "v": "quarterly",
        },
        "PointField": {
            "interactive": {
                "media": {
                    "css": {
                        "dev": ["mapwidgets/css/map_widgets.css"],
                        "minified": ["mapwidgets/css/map_widgets.min.css"],
                    },
                    "js": {
                        "dev": [
                            "mapwidgets/js/mw_init.js",
                            "mapwidgets/js/pointfield/interactive/mw_pointfield_base.js",
                            "mapwidgets/js/pointfield/interactive/googlemap/mw_pointfield.js",
                        ],
                        "minified": [
                            "mapwidgets/js/pointfield/interactive/googlemap/mw_pointfield.min.js"
                        ],
                    },
                },
                "mapOptions": {
                    "zoom": 12,
                    "scrollwheel": False,
                    "streetViewControl": True,
                    "center": get_default_center_coordinates(),
                },
                "GooglePlaceAutocompleteOptions": {},
                "mapCenterLocationName": None,
                "markerFitZoom": 14,
            },
            "static": {
                "enableMagnificPopup": True,
                "thumbnailSize": None,
                "mapParams": {
                    "zoom": 15,
                    "size": "480x480",
                    "scale": "",
                    "format": "",
                    "maptype": "",
                    "language": "",
                    "region": "",
                    "map_id": "",
                    "visible": "",
                    "style": "",
                },
                "markers": {"size": "", "color": "", "icon": ""},
            },
        },
    },
    "Mapbox": {
        "accessToken": None,
        "username": None,
        "PointField": {
            "interactive": {
                "media": {
                    "css": {
                        "dev": ["mapwidgets/css/map_widgets.css"],
                        "minified": ["mapwidgets/css/map_widgets.min.css"],
                    },
                    "js": {
                        "dev": [
                            "mapwidgets/js/mw_init.js",
                            "mapwidgets/js/pointfield/interactive/mw_pointfield_base.js",
                            "mapwidgets/js/pointfield/interactive/mapbox/mw_pointfield.js",
                        ],
                        "minified": [
                            "mapwidgets/js/pointfield/interactive/mapbox/mw_pointfield.min.js"
                        ],
                    },
                },
                "markerFitZoom": 14,
                "showZoomNavigation": True,
                "mapOptions": {
                    "zoom": 12,
                    "style": "mapbox://styles/mapbox/streets-v11",
                    "scrollZoom": False,
                    "animate": False,
                    "center": get_default_center_coordinates(),
                },
                "geocoderOptions": {},
            },
            "static": {
                "enableMagnificPopup": True,
                "thumbnailSize": None,
                "mapParams": {
                    "username": "mapbox",
                    "zoom": 15,
                    "bearing": 0,
                    "pitch": 0,
                    "style_id": "streets-v12",
                    "@2x": "@2x",
                    "width": "480",
                    "height": "480",
                },
                "overlayParams": {"name": "pin-l", "label": "", "color": ""},
            },
        },
    },
    "Leaflet": {
        "PointField": {
            "interactive": {
                "media": {
                    "css": {
                        "dev": ["mapwidgets/css/map_widgets.css"],
                        "minified": ["mapwidgets/css/map_widgets.min.css"],
                    },
                    "js": {
                        "dev": [
                            "mapwidgets/js/mw_init.js",
                            "mapwidgets/js/pointfield/interactive/mw_pointfield_base.js",
                            "mapwidgets/js/pointfield/interactive/leaflet/mw_pointfield.js",
                        ],
                        "minified": [
                            "mapwidgets/js/pointfield/interactive/leaflet/mw_pointfield.min.js"
                        ],
                    },
                },
                "mapOptions": {
                    "zoom": 12,
                    "scrollWheelZoom": False,
                    "zoomControl": True,
                },
                "tileLayer": {
                    "urlTemplate": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                    "options": {"maxZoom": 20},
                },
                "markerFitZoom": 14,
                "showZoomNavigation": True,
                "mapCenterLocation": get_default_center_coordinates(),
            }
        }
    },
    "srid": 4326,
    "is_dev_mode": django_settings.DEBUG,
}


class DotDict(dict):
    """
    A dictionary that allows accessing keys using dot notation and is JSON serializable.
    """

    def __getattr__(self, attr):
        try:
            value = self[attr]
        except KeyError:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{attr}'"
            )

        if isinstance(value, dict):
            return DotDict(value)
        else:
            return value

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __iter__(self):
        return iter(self)

    def items(self):
        for key, value in super().items():
            if isinstance(value, dict):
                value = DotDict(value)
            yield key, value

    def copy(self):
        return DotDict(super().copy())

    def update(self, other=None, **kwargs):
        if other is not None:
            if isinstance(other, dict):
                for key, value in other.items():
                    if (
                        isinstance(value, dict)
                        and key in self
                        and isinstance(self[key], dict)
                    ):
                        self[key] = DotDict(self[key])
                        self[key].update(value)
                    else:
                        self[key] = value
            else:
                raise TypeError(f"'{type(other).__name__}' object is not iterable")
        for key, value in kwargs.items():
            if isinstance(value, dict) and key in self and isinstance(self[key], dict):
                self[key] = DotDict(self[key])
                self[key].update(value)
            else:
                self[key] = value


class MapWidgetSettings(DotDict):
    """
    A class for merging and accessing map widget settings using dot notation.

    This class inherits from `DotDict`, allowing access to dictionary keys using
    dot notation (e.g., `settings.GoogleMap.PointField.interactive`).

    It merges two dictionaries: `default_settings` and `app_settings`.
    `app_settings` takes precedence over `default_settings`.

    If `app_settings` is not provided as argument, it uses the `MAP_WIDGETS`
    setting from the Django settings module.

    The `merge_dict` method recursively merges nested dictionaries, with
    `app_settings` values taking precedence.

    Example:
    >>> settings = MapWidgetSettings()
    >>> settings.GoogleMap.PointField.interactive.markerFitZoom
    14
    """

    def __init__(self, default_settings=None, app_settings=None):
        _django_settings = getattr(django_settings, "MAP_WIDGETS", {})
        app_settings = app_settings if app_settings is not None else _django_settings
        default_settings = (
            default_settings if default_settings is not None else DEFAULT_SETTINGS
        )

        merged = self.merge_dict(default_settings, app_settings)
        super().__init__(merged)

    @classmethod
    def merge_dict(cls, dict1, dict2):
        merged = dict1.copy()
        for key, val in dict2.items():
            if isinstance(val, dict):
                if key in merged and isinstance(merged[key], dict):
                    merged[key] = cls.merge_dict(merged[key], val)
                else:
                    merged[key] = val
            else:
                merged[key] = val
        return merged


mw_settings = MapWidgetSettings(default_settings=DEFAULT_SETTINGS)


def reload_widget_settings(*args, **kwargs):
    global mw_settings
    setting, value = kwargs["setting"], kwargs["value"]
    if setting == "MAP_WIDGETS" and value:
        mw_settings = MapWidgetSettings(
            default_settings=DEFAULT_SETTINGS, app_settings=value
        )


setting_changed.connect(reload_widget_settings)
