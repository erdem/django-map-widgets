.. _google_point_field_map_widgets:

Google Map Interactive Point Field Widget
=========================================

Preview
^^^^^^^

.. image:: ../_static/images/google-point-field-map-widget.gif


Google Map APIs Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To use this widget, you need to enable the following Google APIs in your Google application configuration:

- `Google Maps JavaScript API <https://console.cloud.google.com/apis/library/maps-backend.googleapis.com>`_
- `Places API <https://console.cloud.google.com/apis/library/places-backend.googleapis.com>`_
- `Geocoding API <https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com>`_


Key Features
^^^^^^^^^^^^

**Geocoding:** The widget has built-in geocoding support. The autocomplete input will be filled by the `Google Geocoding <https://developers.google.com/maps/documentation/javascript/geocoding/>`_ service when the user manually adds a marker to the map.

**Reverse Geocoding:** The address search input will also be populated by the Geocoding API when users manually add a marker to the map.

**Dynamic Django Admin Inline Support:** A new widget can be initialized when a new row is added in Django admin inlines. See the usage below.

**Use My Location Action:** Users can set their current location as a marker using the "Use My Location" action button.

**Edit Coordinates Inputs:** The marker coordinates can be updated manually through the `Coordinates` pop-up inputs.

**Draggable Markers:** Positioned markers can be dragged across the map, and the coordinates and geocoding data will be updated when the marker is dropped.

**Add Marker by Click:** Point markers can be added via mouse click.

Settings
^^^^^^^^

`Default Settings Values`

.. code-block:: python
    MAP_WIDGETS = {
        "GoogleMap": {
            "apiKey": None,
            # https://maps.googleapis.com/maps/api/js?language={}&libraries={}&key={}&v={}"
            "CDNURLParams": {
                "language": "en",
                "libraries": "places,marker",
                "loading": "async",
                "v": "quarterly",
            },
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
        }


.. Tip::
    More details about map widget settings usage can be found in the `settings guide <http://django-map-widgets.readthedocs.io/settings>`_.


* **apiKey**: `Google JavaScript API <https://developers.google.com/maps/documentation/javascript/get-api-key/>`_ key. (required)

* **CDNURLParams**: The Google JavaScript API library JS source URL parameters can be modified using this setting.

* **mapOptions**: GoogleMap `MapOptions <https://developers.google.com/maps/documentation/javascript/reference/map#MapOptions>`_ settings can be managed using this dictionary. These settings are passed as arguments to the GoogleMap JS initialization function. Default values are provided for `zoom`, `scrollwheel`, `streetViewControl`, and `center`.

* **mapCenterLocationName**: A specific location name for the center of the map can be provided. The widget will use `Google Place Autocomplete <https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete/>`_ to find the coordinates for this location.

* **markerFitZoom**: A custom zoom value is set programmatically after a marker is added with user geolocation or place autocomplete. This setting exists to enhance the user experience. The default value is 14.


Usage
^^^^^

In the Django project settings file, the `MAP_WIDGETS` dictionary should be defined to customize the default settings for map widgets.

.. code-block:: python

    MAP_WIDGETS = {
        "GoogleMap": {
            "apiKey": GOOGLE_MAP_API_KEY, # your google API
            "PointField": {
                "interactive": {
                    "mapOptions": {
                        "zoom": 15  # default map initial zoom,
                        "scrollwheel": False,
                        "streetViewControl": True
                    },
                    "GooglePlaceAutocompleteOptions": {
                        "componentRestrictions": {"country": "uk"}
                    },
                    "mapCenterLocationName": "London"
                },
            },
        },
    }

**Django Admin**

.. code-block:: python
    import mapwidgets

    class CityAdmin(admin.ModelAdmin):
        list_display = ("name",)
        formfield_overrides = {
            models.PointField: {"widget": mapwidgets.GoogleMapPointFieldWidget}
        }

**Django Forms**

.. code-block:: python
    import mapwidgets

    class CityAdminForm(forms.ModelForm):
        class Meta:
            model = City
            fields = ("coordinates", "city_hall")
            widgets = {
                'coordinates': mapwidgets.GoogleMapPointFieldWidget,
                'city_hall': mapwidgets.GoogleMapPointFieldWidget,
            }


Dynamic Django Admin Inline Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^




Javascript Triggers
^^^^^^^^^^^^^^^^^^^

If you need to develop your map UI on the front-end side, you can use map widget jQuery triggers. See the usages in the `demo project <https://github.com/erdem/django-map-widgets/tree/master/demo>`_.

* **googleMapPointFieldWidget:markerCreate**: Triggered when user creates a marker on the map. (callback params: place, lat, lng, locationInputElem, mapWrapID)

* **googleMapPointFieldWidget:markerChange**: Triggered when user changes marker position on the map. (callback params: place, lat, lng, locationInputElem, mapWrapID)

* **googleMapPointFieldWidget:markerDelete**: Triggered when user deletes marker on the map. (callback params: lat, lng, locationInputElem, mapWrapID)

* **googleMapPointFieldWidget:placeChanged**: Triggered when the place changes in the autocomplete input. (callback params: place, lat, lng, locationInputElem, mapWrapID)

.. code-block:: javascript

    (function ($) {
        $(document).on("googleMapPointFieldWidget:markerCreate", function (e, lat, lng, locationInputElem, mapWrapID) {
            console.log("EVENT: marker_create"); // django widget textarea widget (hidden)
            console.log(locationInputElem); // django widget textarea widget (hidden)
            console.log(lat, lng); // created marker coordinates
            console.log(mapWrapID); // map widget wrapper element ID
        });

        $(document).on("googleMapPointFieldWidget:markerChange", function (e, lat, lng, locationInputElem, mapWrapID) {
            console.log("EVENT: marker_change"); // django widget textarea widget (hidden)
            console.log(locationInputElem); // django widget textarea widget (hidden)
            console.log(lat, lng);  // changed marker coordinates
            console.log(mapWrapID); // map widget wrapper element ID
        });

        $(document).on("googleMapPointFieldWidget:markerDelete", function (e, lat, lng, locationInputElem, mapWrapID) {
            console.log("EVENT: marker_delete"); // django widget textarea widget (hidden)
            console.log(locationInputElem); // django widget textarea widget (hidden)
            console.log(lat, lng);  // deleted marker coordinates
            console.log(mapWrapID); // map widget wrapper element ID
        })

        $(document).on("googleMapPointFieldWidget:placeChanged", function (e, place, lat, lng, locationInputElem, mapWrapID) {
            console.log("EVENT: place_changed"); // django widget textarea widget (hidden)
            console.log(place);
            console.log(locationInputElem); // django widget textarea widget (hidden)
            console.log(lat, lng); // created marker coordinates
            console.log(mapWrapID); // map widget wrapper element ID
        });
        console.log($("#location-map-elem").data("mwMapObj")); // GoogleMap JS object
        console.log($("#location-map-elem").data("mwClassObj")); // the widget class instance object
    })(jQuery)
