---
type: minor
---

Add Django 6.0 compatibility. Django 6.0 removed `id` and `name` from template context in `BaseGeometryWidget.get_context()`. Re-inject these in `BasePointFieldInteractiveWidget.get_context()` for all interactive widgets (Google Maps, Leaflet, Mapbox). Also lift `js_widget_data` and `is_formset_empty_form_template` attrs to top-level context in `PointFieldInlineWidgetMixin.get_context()` for inline formset widgets.
