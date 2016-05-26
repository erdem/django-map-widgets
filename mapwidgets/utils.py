import json

from django.conf import settings


DEFAULT_MAP_OPTIONS = {
    "mapApiKey": "",
    "mapCenterLocationName": None, # todo is empty find from django timezone
    "mapCenterLocation": None,  # todo is empty find from django timezone
    "zoom": 6,
}


# todo use signleton pattern
def get_map_options():
    default_options = DEFAULT_MAP_OPTIONS.copy()
    user_options = getattr(settings, "MAP_WIDGET_OPTIONS", {})
    default_options.update(user_options)
    return json.dumps(default_options)


def get_google_api_key():
    return settings.MAP_WIDGET_OPTIONS.get("mapApiKey", "")