Static Point Field Widget
=========================

**Preview**

.. image:: ../_static/images/google-point-static-map-widget.png

Django map widgets provide all Google Static Map API features. Check out this `link <https://developers.google.com/maps/documentation/static-maps/intro>`_ for the google static map API features.

Here is the all default settings attribute for google static map widget.


.. code-block:: python

    MAP_WIDGETS = {
        "GoogleStaticMapWidget": {
            "zoom": 15,
            "size": "480x480",
            "scale": "",
            "format": "",
            "maptype": "",
            "path": "",
            "visible": "",
            "style": "",
            "language": "",
            "region": ""
        },

        "GoogleStaticMapMarkerSettings": {
            "size": "normal",
            "color": "",
            "icon": "",
        },
        "LANGUAGE": "en",
        "GOOGLE_MAP_API_SIGNATURE": "",
        "GOOGLE_MAP_API_KEY": "",
    }

**Usage**

If you are not using specific features on Google Static Map API, you just need to update GOOGLE_MAP_API_KEY value in your Django settings file. If you also need individual size map images, you can pass `size` and `zoom` parameter for each GoogleStaticMapWidget class.

Google Map APIs configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In order to use this widget, you need to enable Google Map static API in your google application configuration;

- `Google Maps Static API <https://console.cloud.google.com/apis/library/static-maps-backend.googleapis.com>`_

**Settings**

In your ``settings.py`` file, add your ``MAP_WIDGETS`` config:

.. code-block:: python

    MAP_WIDGETS = {
        "GoogleStaticMapWidget": {
            "zoom": 15,
            "size": "320x320",
        },
        "GoogleStaticMapMarkerSettings": {
            "color": "green",
        },
        "GOOGLE_MAP_API_KEY": "<google-map-api-key>"
    }


**Django Admin**

.. code-block:: python

    from mapwidgets.widgets import GoogleStaticMapWidget

    class CityAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.PointField: {"widget": GoogleStaticMapWidget}
        }


**Django Forms**


.. code-block:: python

    from mapwidgets.widgets import GoogleStaticMapWidget

    class CityDetailForm(forms.ModelForm):

        class Meta:
            model = City
            fields = "name": "coordinates", "city_hall"
            widgets = {
                'coordinates': GoogleStaticMapWidget,
                'city_hall': GoogleStaticMapWidget(zoom=12, size="240x240"),
            }





**Preview**

.. image:: ../_static/images/google-point-static-overlay-map-widget.png

This widget is working with `Magnific Popup <http://dimsemenov.com/plugins/magnific-popup/>`_  jQuery plugin. The plugin javascript file load with the widget static files.

**Usage**

You can also use all static map features in this widget. Besides you can give a ``thumbnail_size`` value.

Here is the all default settings attribute for google static overlay map widget.

.. code-block:: python

    MAP_WIDGETS = {
        "GoogleStaticMapMarkerSettings": {
            "size": "normal",
            "color": "",
            "icon": ""
        },

        "GoogleStaticOverlayMapWidget": {
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
            "region": ""
        },

        "GOOGLE_MAP_API_SIGNATURE": "",
        "GOOGLE_MAP_API_KEY": "",
    }

Google Map APIs configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In order to use this widget, you need to enable Google Map static API in your google application configuration;

- `Google Maps Static API <https://console.cloud.google.com/apis/library/static-maps-backend.googleapis.com>`_


**Settings**

In your django ``settings.py`` file, add your ``MAP_WIDGETS`` config:

.. code-block:: python

    MAP_WIDGETS = {
        "GoogleStaticMapWidget": {
            "zoom": 15,
            "size": "320x320",
            "thumbnail_size": "100x100",
        },
        "GoogleStaticMapMarkerSettings": {
            "color": "green",
        },
        "GOOGLE_MAP_API_KEY": "<google-map-api-key>"
    }


**Django Admin**

.. code-block:: python

    from mapwidgets.widgets import GoogleStaticOverlayMapWidget

    class CityAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.PointField: {"widget": GoogleStaticOverlayMapWidget}
        }


**Django Forms**


.. code-block:: python

    from mapwidgets.widgets import GoogleStaticOverlayMapWidget

    class CityDetailForm(forms.ModelForm):

        class Meta:
            model = City
            fields = "name": "coordinates", "city_hall"
            widgets = {
                'coordinates': GoogleStaticOverlayMapWidget,
                'city_hall': GoogleStaticOverlayMapWidget(zoom=12, size="240x240"),
            }

