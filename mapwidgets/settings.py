from django.conf import settings

from mapwidgets.constants import TIMEZONE_COORDINATES

DEFAULT_MAP_SETTINGS = {
    "GOOGLE_MAP_API_KEY": "",
    "mapCenterLocationName": None,  # todo is empty find from django timezone
    "mapCenterLocation": TIMEZONE_COORDINATES.get(getattr(settings, "TIME_ZONE", "UTC")),  # todo is empty find from django timezone
    "zoom": 6,
}

print DEFAULT_MAP_SETTINGS

class MapWidgetSettings(object):

    def __init__(self):
        user_settings = getattr(settings, "MAP_WIDGETS", {})
        default_settings = DEFAULT_MAP_SETTINGS.copy()
        default_settings.update(user_settings)
        self._map_settings = default_settings

    @property
    def map_conf(self):
        return self._map_settings

    def __getattr__(self, attr):
        if attr not in self._map_settings.keys():
            raise AttributeError("Invalid Django Map Widgets setting: '%s'" % attr)

        return self._map_settings.get(attr)

mw_settings = MapWidgetSettings()
