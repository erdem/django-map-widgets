---
type: minor
---

Add reverse geocoding to `LeafletPointFieldWidget` (point field only). When a point is set on the map — including a saved value loaded from the database, or after click/drag/geolocation — the marker location is reverse geocoded via [leaflet-control-geocoder](https://github.com/perliedman/leaflet-control-geocoder) and the resolved place name is shown in the search bar, mirroring the Google point widget. Toggle with the new `geoSearch.reverseGeocode` setting (default `True`; OpenStreetMap/Nominatim, no API key). Also fixes the Leaflet point widget delete action clearing the (now wired) search input.
