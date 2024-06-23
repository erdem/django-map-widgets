.. _settings:

========
Settings
========

In your Django project settings file, define the ``MAP_WIDGETS`` dictionary to customize the default settings for map widgets. The settings are organized using a nested hierarchical structure, which allows for granular control at multiple levels:

    *Global Settings* >> *Map Provider Name* >> *GeoField type* >> *Widget type(interactive or static)*.


This approach ensures that you can configure each aspect of the map widget's functionality precisely according to your needs.


Here is an example of how the settings might be configured:


.. code-block:: python

    MAP_WIDGETS = {
        "GoogleMap": {
            "apiKey": GOOGLE_MAP_API_KEY,  # General setting for all GoogleMap widgets
            "PointField": {   # GeoField type
                "interactive": {  # Specific settings for GoogleMap interactive PointField widget
                    "mapOptions": {
                        "zoom": 15,
                    },
                    "GooglePlaceAutocompleteOptions": {
                        "componentRestrictions": {"country": "uk"}
                    },
                    "mapCenterLocationName": "london",
                }
            },
        },
        "Mapbox": {
            "accessToken": MAPBOX_ACCESS_TOKEN,
            "PointField": {
                "interactive": {
                    "mapOptions": {"zoom": 12, "center": (51.515618, -0.091998)},
                    "markerFitZoom": 14,
                }
            },
        },
        "is_dev_mode": False,  # Package global level setting for development mode
    }



Customizing Individual Widget Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can customize specific widget settings by providing a dictionary with the settings you want to override. These custom settings will be merged with the project settings, allowing for fine-grained control without overwriting the entire configuration.

For example, to customize a standalone ``GoogleMapPointFieldWidget`` to enable the ``scrollwheel`` option:


.. code-block:: python

    from django.contrib.gis import forms
    from mapwidgets.widgets import GooglePointFieldWidget

    CUSTOM_MAP_SETTINGS = {"mapOptions": {"scrollwheel": True}}

    class AnyAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.PointField: {"widget": GooglePointFieldWidget(settings=CUSTOM_MAP_SETTINGS)}
        }

    # after settings merge, the widget `mapOptions` settings will be
    #"mapOptions": {
    #    "zoom": 15,
    #    "streetViewControl": False,
    #    "scrollwheel": True,
    #    "fullscreenControl": False,
    #},

This will merge the custom settings with the existing settings, ensuring that only the specified options are overridden.

Remember to ensure that your custom settings follow the nested structure used in the ``MAP_WIDGETS`` dictionary to correctly override the desired attributes. To see full default settings configuration check `mapwidgets/settings.py` file `in the repository <https://github.com/erdem/django-map-widgets/>`_.




