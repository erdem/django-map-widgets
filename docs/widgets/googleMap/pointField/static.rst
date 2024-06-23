Static Point Field Widget
=========================

Preview
^^^^^^^

.. image:: /_static/images/google_static_overlay.png


This widget integrates with Django to provide an interface using the Google
`Maps Static API <https://developers.google.com/maps/documentation/maps-static>`_.
It automatically generates static map images based on GeoDjango PointField values.

Requirements
^^^^^^^^^^^^
To use this widget, you need to enable the following Google APIs in your Google application configuration:

- `Maps Static API <https://developers.google.com/maps/documentation/maps-static>`_


Key Features
^^^^^^^^^^^^

**Generate Static Map Image Automatically:** The widget can generate a static image URL with the provided GeoDjango PointField value.

**MagnificPopup Support:** The widget-generated static map image can work with the `MagnificPopup jQuery Plugin <https://dimsemenov.com/plugins/magnific-popup/>`_.

**Generate Thumbnail for Better Popup Usage:** You can specify a thumbnail size with the `thumbnailSize` setting for better popup usage. Note that this setting will result in an additional API request, which may incur extra costs.

Settings
^^^^^^^^
Default Settings
----------------

.. code-block:: python

    MAP_WIDGETS = {
        "GoogleMap": {
            "apiKey": None,
            "PointField": {
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
                    "markers": {
                        "size": "",
                        "color": "",
                        "icon": ""
                    },
                },
            },
        }
    }

* **apiKey**: `Google JavaScript API <https://developers.google.com/maps/documentation/javascript/get-api-key/>`_ key. (required)

* **enableMagnificPopup**: Enable/Disable `MagnificPopup <https://dimsemenov.com/plugins/magnific-popup/>`_ functionality.

* **thumbnailSize**: Specify thumbnail size for better popup usage.(e.g ``240x240``)

* **mapParams**: Static Map Image API `MapParams <https://developers.google.com/maps/documentation/maps-static/start#location>`_ can be managed using this dictionary globally.

* **markers**: The map `marker style <https://developers.google.com/maps/documentation/maps-static/start#MarkerStyles>`_  can be managed using this dictionary globally.

.. Note::
    More details about map widget settings usage can be found in the :ref:`settings guide <settings>`.

Usage
^^^^^

In the Django project settings file, the `MAP_WIDGETS` dictionary should be defined to customize the default settings for map widgets.

.. code-block:: python

    MAP_WIDGETS = {
        "GoogleMap": {
            "apiKey": GOOGLE_MAP_API_KEY,  # Your Google API key
            "PointField": {
                "static": {
                    "thumbnailSize": "240x240",
                    "enableMagnificPopup": True,
                    "mapParams": {
                        "size": "480x480",
                        "zoom": 13
                    },
                    "markers": {
                        "color": "red"
                    }
                },
            },
        },
    }

Django Admin
------------

.. code-block:: python

    from mapwidgets import GoogleMapPointFieldStaticWidget

    class CityAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.PointField: {"widget": GoogleMapPointFieldStaticWidget}
        }

Django Forms
------------

See the `location_has_default` field usage to understand how you can override global settings with the `settings` parameter for a specific widget.

.. code-block:: python

    from mapwidgets import GoogleMapPointFieldStaticWidget

    class CityDetailForm(forms.ModelForm):

        class Meta:
            model = City
            fields = ("name", "location", "location_has_default")
            widgets = {
                "location": GoogleMapPointFieldStaticWidget,
                "location_has_default": GoogleMapPointFieldStaticWidget(
                    settings={"enableMagnificPopup": False}
                ),
            }


See more usage of this widget in `demo project <https://github.com/erdem/django-map-widgets/tree/main/demo>`_.