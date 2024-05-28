.. _google_point_field_map_widgets:

Google Map Point Field Widget
=============================

Preview
^^^^^^^

.. image:: ../_static/images/google-point-field-map-widget.gif


Google Map APIs configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In order to use this widget, you need to enable Google APIs below in your Google application configuration:

- `Google Maps JavaScript API <https://console.cloud.google.com/apis/library/maps-backend.googleapis.com>`_
- `Places API <https://console.cloud.google.com/apis/library/places-backend.googleapis.com>`_
- `Geocoding API <https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com>`_


.. Tip::

    The widget has a Google Place Autocomplete component by default. You can find a specific address coordinates with it.

.. Tip::

    The widget has built-in geocoding support. The autocomplete input will be filled by `google geocoding <https://developers.google.com/maps/documentation/javascript/geocoding/>`_ service when the user adds a marker to map manually.

.. Tip::

    The widget now supports draggable markers, allowing users to refine the location by dragging the marker to the desired position. The coordinates update in real-time.

Settings
^^^^^^^^

.. code-block:: python
    MAP_WIDGETS = {
        "GoogleMap": {
            "apiKey": None, # your google API
            "PointField": {
                "interactive": {
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
            },
        },
    }


* **apiKey**: Google API key (required).

* **GOOGLE_MAP_API_SIGNATURE**: You can provide a Google Static Map API signature key (optional). Check out this `page <https://developers.google.com/maps/documentation/static-maps/get-api-key/>`_.

* **LANGUAGE**: Google Map language (optional, default value is ``en``).

* **mapCenterLocationName**: You can provide a specific location name for the center of the map. The widget will find this location coordinates using `Google Place Autocomplete <https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete/>`_ (optional).

* **mapCenterLocation**: You can provide specific coordinates for the center of the map. Coordinates must be in list format ([latitude, longitude]) (optional).

* **zoom**: Default zoom value for maps (optional, default value is 6).

* **scrollWheel**: Enables or disables zooming on the map using a mouse scroll wheel. Set as `True` in your Django settings to enable it, the scroll wheel zooming is disabled by default.

* **markerFitZoom**: When the marker is initialized, Google's default zoom is set to Max. This method sets the zoom level a reasonable distance and centers the marker on the map.

* **streetViewControl**: Whether or not to display the Street View "Peg Man" (optional, default is ``True``). Setting this to ``False`` effectively disables Street View for the widget.

* **draggableMarker**: Allows the marker to be draggable (optional, default is ``True``). Users can drag the marker to the desired position.

Usage
^^^^^

**Settings**

In your ``settings.py`` file, add your ``MAP_WIDGETS`` config:

.. code-block:: python

    MAP_WIDGETS = {
        "GoogleMap": {
            "apiKey": None, # your google API
            "PointField": {
                "interactive": {
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
            },
        },
    }

If you want to provide specific location name or coordinates for the center of the map, you can update your settings like this:

.. code-block:: python

    MAP_WIDGETS = {
        "GooglePointFieldWidget": (
            ("zoom", 15),
            ("mapCenterLocation", [57.7177013, -16.6300491]),
        ),
        "GOOGLE_MAP_API_KEY": "<google-map-api-key>"
    }

.. code-block:: python

    MAP_WIDGETS = {
        "GooglePointFieldWidget": (
            ("zoom", 15),
            ("mapCenterLocationName", 'Canada'),
        ),
        "GOOGLE_MAP_API_KEY": "<google-map-api-key>"
    }

.. Tip::

    If there is no specific value set for the map center for ``mapCenterLocationName`` or ``mapCenterLocation``, the widget will be centered by the timezone setting of the project. Check out these links:

    * `Timezone Center Locations <https://github.com/erdem/django-map-widgets/blob/master/mapwidgets/constants.py/>`_
    * `countries.json <https://github.com/erdem/django-map-widgets/blob/master/mapwidgets/constants.py/>`_

You can also provide specific `settings` as a parameter for each widget.

.. Note::

    Google Map is using SRID (Spatial Reference System Identifier) as `4326`, the same as Django’s default SRID value for PostGIS fields. If you set the SRID parameter on a PostGIS field, the coordinates will be stored in your SRID format in your database, but the widget always converts coordinates to `4326` format when rendering. Because the Google Map JavaScript API uses `4326` format, you may see different coordinate values on the frontend compared to your database, but the point will always represent the same location. More information is available on this `Wikipedia page <https://en.wikipedia.org/wiki/Spatial_reference_system>`_.

.. code-block:: python

    from django.contrib.gis import forms
    from mapwidgets.widgets import GooglePointFieldWidget

    CUSTOM_MAP_SETTINGS = {
        "GooglePointFieldWidget": (
            ("zoom", 15),
            ("mapCenterLocation", [60.7177013, -22.6300491]),
        ),
    }

    class CityAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.PointField: {"widget": GooglePointFieldWidget(settings=CUSTOM_MAP_SETTINGS)}
        }

.. Note::

    `GOOGLE_MAP_API_KEY` must be set in the project Django settings file for custom settings usage.

**Django Admin**

.. code-block:: python

    from mapwidgets.widgets import GooglePointFieldWidget

    class CityAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.PointField: {"widget": GooglePointFieldWidget}
        }

**Django Forms**

.. code-block:: python

    from mapwidgets.widgets import GooglePointFieldWidget

    class CityAdminForm(forms.ModelForm):
        class Meta:
            model = City
            fields = ("coordinates", "city_hall")
            widgets = {
                'coordinates': GooglePointFieldWidget,
                'city_hall': GooglePointFieldWidget,
            }

Javascript Triggers
^^^^^^^^^^^^^^^^^^^

If you need to develop your map UI on the front-end side, you can use map widget jQuery triggers.

* **google_point_map_widget:marker_create**: Triggered when user creates a marker on the map. (callback params: place, lat, lng, locationInputElem, mapWrapID)

* **google_point_map_widget:marker_change**: Triggered when user changes marker position on the map. (callback params: place, lat, lng, locationInputElem, mapWrapID)

* **google_point_map_widget:marker_delete**: Triggered when user deletes marker on the map. (callback params: lat, lng, locationInputElem, mapWrapID)

* **google_point_map_widget:place_changed**: Triggered when the place changes in the autocomplete input. (callback params: place, lat, lng, locationInputElem, mapWrapID)

.. code-block:: javascript

      (function ($){
          $(document).on("google_point_map_widget:marker_create", function (e, lat, lng, locationInputElem, mapWrapID) {
              console.log("EVENT: marker_create");
              console.log(locationInputElem);
              console.log(lat, lng);
              console.log(mapWrapID);
          });

          $(document).on("google_point_map_widget:marker_change", function (e, lat, lng, locationInputElem, mapWrapID) {
              console.log("EVENT: marker_change");
              console.log(locationInputElem);
              console.log(lat, lng);
              console.log(mapWrapID);
          });

          $(document).on("google_point_map_widget:marker_delete", function (e, lat, lng, locationInputElem, mapWrapID) {
              console.log("EVENT: marker_delete");
              console.log(locationInputElem);
              console.log(lat, lng);
              console.log(mapWrapID);
          });

          $(document).on("google_point_map_widget:place_changed", function (e, place, lat, lng, locationInputElem, mapWrapID) {
              console.log("EVENT: place_changed");
              console.log(place);
              console.log(locationInputElem
