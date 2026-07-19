---
type: minor
---

Add a location search bar to the Leaflet widgets (both `LeafletPointFieldWidget` and `LeafletPolygonFieldWidget`), powered by [leaflet-geosearch](https://github.com/smeijer/leaflet-geosearch). The search input lives in the widget header (project-styled, with a custom autocomplete dropdown). Selecting a result drops the marker (point widget) or pans/zooms the map to the area (polygon widget). Configurable via the new `geoSearch` setting (`enabled`, `provider`, `providerOptions`); defaults to the free OpenStreetMap/Nominatim provider (no API key), and supports any leaflet-geosearch provider (Google, Mapbox, Esri, ...) via settings.
