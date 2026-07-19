Interactive Point Field Widget
==============================

Preview
^^^^^^^

.. image:: /_static/images/leaflet_point_interactive.png


Requirements
^^^^^^^^^^^^
There is no requirements to use `Leaflet <https://leafletjs.com/>`_ open-source interactive map JavaScript library.


Key Features
^^^^^^^^^^^^

**Use My Location Action:** Users can set their current location as a marker using the "Use My Location" action button.

**Edit Coordinates Inputs:** The marker coordinates (latitude, longitude) can be updated manually through the `Coordinates` dropdown pop-up inputs.

**Draggable Markers:** Positioned markers can be dragged across the map, and the coordinates inputs will be updated when the marker is dropped.

**Add Marker by Click:** A marker can be added to the map via mouse click.

**Location Search:** A search bar (powered by `leaflet-geosearch <https://github.com/smeijer/leaflet-geosearch>`_) lets users find a place by name/address; selecting a result drops the marker there. Configurable via the ``geoSearch`` setting (default provider: OpenStreetMap / Nominatim, no API key required).

**Reverse Geocoding:** When a point is set on the map (including a saved value loaded from the database, or after click/drag/geolocation), the marker location is reverse geocoded (via `leaflet-control-geocoder <https://github.com/perliedman/leaflet-control-geocoder>`_) and the resolved place name is shown in the search bar. Toggle with ``geoSearch.reverseGeocode`` (default ``True``).


Settings
^^^^^^^^
``Default Settings``

.. code-block:: python

    MAP_WIDGETS = {
        "Leaflet": {
            "PointField": {
                "mapOptions": {"zoom": 12, "scrollWheelZoom": False},
                "tileLayer": {
                    "urlTemplate": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                    "options": {"maxZoom": 20},
                },
                "markerFitZoom": 14,
                "showZoomNavigation": True,
                "mapCenterLocation": get_default_center_coordinates(),
                }
            }
        }
    }



* **mapOptions**: Leaflet `MapOptions <https://leafletjs.com/reference.html#map-option>`_ settings can be managed using this dictionary. These settings are passed as arguments to Leaflet JS initialization function. Default values are provided for `zoom`, `scrollWheelZoom`.

* **tileLayer**: TileLayer source configuration. (Do not override the default settings if you don't serve the map tiles from different source ``openstreetmap.org``)
* **markerFitZoom**: A custom zoom value is set programmatically after a marker is added with user geolocation or place autocomplete so on. This setting exists to enhance the user experience. The default value is 14.
* **geoSearch**: Location search bar configuration. ``enabled`` (default ``True``) toggles the search input; ``provider`` is the `leaflet-geosearch <https://github.com/smeijer/leaflet-geosearch>`_ provider class name (default ``"OpenStreetMapProvider"``; others include ``"GoogleProvider"``, ``"MapBoxProvider"``, ``"EsriProvider"``, ...); ``providerOptions`` is passed to the provider constructor (e.g. ``{"params": {"key": "YOUR_API_KEY"}}`` for keyed providers); ``reverseGeocode`` (default ``True``) reverse geocodes the marker location to populate the search bar with the place name.
* **showZoomNavigation**: Enable/Disable zoom in/out UI buttons on the map. Default is ``True``
* **mapCenterLocation**: Enable zoom in/out UI buttons on the map. Default is ``True``


.. Note::
    More details about map widget settings usage can be found in the :ref:`settings guide <settings>`.

.. Note::

    If no settings are provided for the map center (``mapCenterLocation``), the map will automatically center based on the django project's timezone setting. This feature ensures that the map displays an appropriate and relevant initial view.

    For more details on timezone center coordinates, refer to the following resources:

    * `Timezone Center Locations <https://github.com/erdem/django-map-widgets/blob/master/mapwidgets/constants.py/>`_
    * `countries.json <https://github.com/erdem/django-map-widgets/blob/master/mapwidgets/constants.py/>`_


Usage
^^^^^

In the Django project settings file, the `MAP_WIDGETS` dictionary should be defined to customize the default settings for map widgets.

.. code-block:: python

    MAP_WIDGETS = {
        "Leaflet": {
            "PointField": {
                "mapOptions": {"scrollWheelZoom": True},
                "showZoomNavigation": False,
            }
        }
    }

**Django Admin**

.. code-block:: python
    import mapwidgets

    class CityAdmin(admin.ModelAdmin):
        list_display = ("name",)
        formfield_overrides = {
            models.PointField: {"widget": mapwidgets.LeafletPointFieldWidget}
        }

**Django Forms**

.. code-block:: python
    import mapwidgets

    class CityAdminForm(forms.ModelForm):
        class Meta:
            model = City
            fields = ("coordinates", "city_hall")
            widgets = {
                'coordinates': mapwidgets.LeafletPointFieldWidget,
                'city_hall': mapwidgets.LeafletPointFieldWidget,
            }



Javascript Triggers
^^^^^^^^^^^^^^^^^^^

There is no jQuery event trigger support for this widget yet.
