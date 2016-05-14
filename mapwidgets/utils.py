from django.conf import settings


DEFAULT_MAP_OPTIONS = {
    "zoom": 3,
}

# todo use signleton pattern
def get_map_options():
    default_options = DEFAULT_MAP_OPTIONS.copy()
    user_options = getattr(settings, "MAP_WIDGET_OPTIONS", {})
    default_options.update(user_options)
    return default_options
