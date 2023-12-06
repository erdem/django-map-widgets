Settings for Map Widgets
========================


In the django project settings file, define your ``MAP_WIDGETS`` dict type config if you want to override the default settings for map widgets.

Basically, the settings for map widgets are defined in a dictionary format. Each key in the dictionary represents a specific widget type.

Overview
--------

The settings for map widgets are defined in a dictionary format. Each key in the dictionary represents a specific widget type.

Example
-------

Here is an example of how the settings might be configured:

.. code-block:: python

    MAP_WIDGETS = {
        "GooglePointFieldWidget": {
            "zoom": 15,
            "mapCenterLocation": [51.5074, -0.1278],
            "markerFitZoom": 12,
            "GooglePlaceAutocompleteOptions": {'componentRestrictions': {'country': 'uk'}},
            "scrollWheel": True,
            "streetViewControl": False,
        },
        "MapboxPointFieldWidget": {
            "access_token": "<mapbox-access-token>",
            "mapOptions": {
                "zoom": 10,
                "center": [51.5074, -0.1278]
            }
        },
        "GOOGLE_MAP_API_KEY": "<google-map-api-key>"
    }

Customizing Widget Settings in Django Admin
-------------------------------------------

You can also customize the settings for a specific widget instance in the Django Admin. This is useful when you need to override the specif global settings attribute for a particular use-case. The settings provided at the widget level will override the general settings configured in the `MAP_WIDGETS`.

Here's an example:

.. code-block:: python

    from django.contrib.gis import forms
    from mapwidgets.widgets import GooglePointFieldWidget

    CUSTOM_MAP_SETTINGS = {
        "GooglePointFieldWidget": {
            "zoom": 15,
            "mapCenterLocation": [60.7177013, -22.6300491],
        },
    }

    class CityAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.PointField: {"widget": GooglePointFieldWidget(settings=CUSTOM_MAP_SETTINGS)}
        }