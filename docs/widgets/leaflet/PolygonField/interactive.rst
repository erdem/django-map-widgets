Interactive Polygon Field Widget
================================

A widget for GeoDjango ``PolygonField`` built on the `Leaflet <https://leafletjs.com/>`_
open-source map library. It keeps the same UX elements as the Leaflet Point Field widget
(toolbar buttons, footer delete action) and draws polygons using pure Leaflet — no extra
JavaScript dependency.

Preview
^^^^^^^

.. image:: /_static/images/leaflet_polygon_interactive.png



Requirements
^^^^^^^^^^^^
There is no requirement to use `Leaflet <https://leafletjs.com/>`_ open-source interactive map JavaScript library.


Key Features
^^^^^^^^^^^^

**Draw Polygon Action:** Click the "Draw Polygon" button to enter drawing mode, then click the map
to drop vertices. Close the ring by clicking the first vertex or double-clicking the map.

**Editable Vertices:** Once a polygon is created, each vertex is a draggable handle. Dragging a
vertex reshapes the polygon and updates the field value.

**Edit Coordinates:** The "Edit Coordinates" dropdown exposes a textarea showing the polygon as WKT.
You can paste a ``POLYGON((...))`` (WKT) and press "Done" to render it.

**Use My Location Action:** Recenters the map on the user's current location.

**Location Search:** A search bar (powered by `leaflet-geosearch <https://github.com/smeijer/leaflet-geosearch>`_) lets users find a place by name/address; selecting a result pans/zooms the map there so the area can be drawn. Configurable via the ``geoSearch`` setting (default provider: OpenStreetMap / Nominatim, no API key required).


Settings
^^^^^^^^
``Default Settings``

.. code-block:: python

    MAP_WIDGETS = {
        "Leaflet": {
            "PolygonField": {
                "mapOptions": {"zoom": 12, "scrollWheelZoom": False, "zoomControl": True},
                "tileLayer": {
                    "urlTemplate": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                    "options": {"maxZoom": 20},
                },
                "polygonOptions": {"color": "#3388ff", "weight": 3, "fillOpacity": 0.2},
                "polygonFitZoom": 14,
                "fitBoundsOnLoad": True,
                "showZoomNavigation": True,
                "mapCenterLocation": get_default_center_coordinates(),
            }
        }
    }


* **mapOptions**: Leaflet `MapOptions <https://leafletjs.com/reference.html#map-option>`_ passed to the Leaflet map initialization.
* **tileLayer**: TileLayer source configuration. (Do not override the default settings unless you serve the map tiles from a different source than ``openstreetmap.org``.)
* **polygonOptions**: Leaflet `Path <https://leafletjs.com/reference.html#path>`_ styling for the rendered polygon (``color``, ``weight``, ``fillOpacity``).
* **geoSearch**: Location search bar configuration. ``enabled`` (default ``True``) toggles the search input; ``provider`` is the `leaflet-geosearch <https://github.com/smeijer/leaflet-geosearch>`_ provider class name (default ``"OpenStreetMapProvider"``); ``providerOptions`` is passed to the provider constructor (e.g. ``{"params": {"key": "YOUR_API_KEY"}}`` for keyed providers).
* **polygonFitZoom**: Maximum zoom used when fitting the map to the polygon bounds or centering on the user location. Default is 14.
* **fitBoundsOnLoad**: Fit the map to the existing polygon bounds when the widget loads. Default is ``True``.
* **showZoomNavigation**: Enable/Disable zoom in/out UI buttons on the map. Default is ``True``.
* **mapCenterLocation**: Initial map center. Defaults to the project timezone based coordinates.


.. Note::
    More details about map widget settings usage can be found in the :ref:`settings guide <settings>`.


Usage
^^^^^

In the Django project settings file, the ``MAP_WIDGETS`` dictionary can be defined to customize the default settings.

.. code-block:: python

    MAP_WIDGETS = {
        "Leaflet": {
            "PolygonField": {
                "mapOptions": {"scrollWheelZoom": True},
                "polygonOptions": {"color": "#e74c3c", "fillOpacity": 0.3},
            }
        }
    }

**Django Admin**

.. code-block:: python

    import mapwidgets

    class ZoneAdmin(admin.ModelAdmin):
        list_display = ("name",)
        formfield_overrides = {
            models.PolygonField: {"widget": mapwidgets.LeafletPolygonFieldWidget}
        }

**Django Forms**

.. code-block:: python

    import mapwidgets

    class ZoneForm(forms.ModelForm):
        class Meta:
            model = Zone
            fields = ("name", "area")
            widgets = {
                "area": mapwidgets.LeafletPolygonFieldWidget,
            }


Javascript Triggers
^^^^^^^^^^^^^^^^^^^

The widget fires jQuery events on ``document`` when the polygon changes. Each handler receives the
polygon GeoJSON, the widget wrapper selector, and the hidden Django input element.

.. code-block:: javascript

    $(document).on("leafletPolygonFieldWidget:polygonCreate", function (e, geojson, mapWrapSelector, djangoInput) { });
    $(document).on("leafletPolygonFieldWidget:polygonChange", function (e, geojson, mapWrapSelector, djangoInput) { });
    $(document).on("leafletPolygonFieldWidget:polygonDelete", function (e, value, mapWrapSelector, djangoInput) { });
