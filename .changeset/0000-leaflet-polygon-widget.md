---
type: minor
---

Add `LeafletPolygonFieldWidget`, an interactive widget for GeoDjango `PolygonField` built on pure Leaflet (no extra JS dependency). It keeps the existing widget UX: draw a polygon by clicking vertices (close by clicking the first vertex or double-clicking), drag vertices to edit, an "Edit Coordinates" overlay accepting WKT or GeoJSON, "Current Location", and delete. Fires `leafletPolygonFieldWidget:polygonCreate/polygonChange/polygonDelete` jQuery triggers. Adds `Leaflet.PolygonField` settings, a shared `BaseInteractiveGeometryWidget` base, and demo/docs coverage.
