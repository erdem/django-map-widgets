===========
Map Widgets
===========

Django Map Widgets offers two types of widgets:

1. **Interactive (Dynamic) Widgets**: These widgets allow users to interact with the map, such as clicking to set a
   location or dragging a marker. They are ideal for data input and editing scenarios.

2. **Static (Read-only) Widgets**: These widgets display map data in a non-interactive format. They are useful for
   presenting location information without allowing modifications.

**Widget Support Matrix**

+------------------------+-------------+--------+-------------+--------+-------------+--------+
| **GeoDjango Field**    | **GoogleMap**        | **Mapbox**           | **Leaflet**          |
+------------------------+-------------+--------+-------------+--------+-------------+--------+
|                        | Interactive | Static | Interactive | Static | Interactive | Static |
+========================+=============+========+=============+========+=============+========+
| *PointField*           | ✅          | ✅     | ✅          | ✅     | ✅          | N/A    |
+------------------------+-------------+--------+-------------+--------+-------------+--------+
| *LineStringField*      | ✖️          | ✖️     | ✖️          | ✖️     | ✖️          | N/A    |
+------------------------+-------------+--------+-------------+--------+-------------+--------+
| *PolygonField*         | ✖️          | ✖️     | ✖️          | ✖️     | ✖️          | N/A    |
+------------------------+-------------+--------+-------------+--------+-------------+--------+
| *MultiPointField*      | ✖️          | ✖️     | ✖️          | ✖️     | ✖️          | N/A    |
+------------------------+-------------+--------+-------------+--------+-------------+--------+
| *MultiLineStringField* | ✖️          | ✖️     | ✖️          | ✖️     | ✖️          | N/A    |
+------------------------+-------------+--------+-------------+--------+-------------+--------+
| *MultiPolygonField*    | ✖️          | ✖️     | ✖️          | ✖️     | ✖️          | N/A    |
+------------------------+-------------+--------+-------------+--------+-------------+--------+


.. toctree::

    settings
    googleMap/index
    leaflet/index
    mapbox/index
