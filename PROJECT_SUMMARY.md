# Django Map Widgets - Project Summary

## Project Overview
Django Map Widgets is a Django package that provides highly configurable, pluggable, and user-friendly map widgets for GeoDjango form fields. It simplifies the integration of interactive maps into GeoDjango applications, supporting Google Maps, Mapbox, and Leaflet mapping platforms.

## Key Features
- **Interactive (Dynamic) Widgets**: Allow users to interact with maps (click to set location, drag markers)
- **Static (Read-only) Widgets**: Display map data in non-interactive format
- **Multiple Map Providers**: Google Maps, Mapbox, and Leaflet support
- **GeoDjango Integration**: Seamless integration with Django's geographic framework
- **Configurable**: Extensive customization options through settings

## Current Widget Support
- **PointField**: ✅ (GoogleMap, Mapbox, Leaflet - Interactive & Static)
- **LineStringField**: ❌ (Planned for future)
- **PolygonField**: ❌ (Planned for future)
- **MultiPointField**: ❌ (Planned for future)
- **MultiLineStringField**: ❌ (Planned for future)
- **MultiPolygonField**: ❌ (Planned for future)

## Project Structure

### Core Package (`mapwidgets/`)
- `widgets/` - Main widget implementations
  - `base.py` - Base widget classes and mixins
  - `googlemap.py` - Google Maps widgets
  - `mapbox.py` - Mapbox widgets
  - `leaflet.py` - Leaflet widgets
  - `mixins.py` - Reusable widget mixins
- `settings.py` - Configuration handling
- `constants.py` - Application constants
- `utils.py` - Utility functions

### Demo Project (`demo/`)
- Example implementations for all three map providers
- Admin integration examples
- Form usage examples
- Testing and development environment

### Documentation (`docs/`)
- Sphinx-based documentation
- Usage examples and API reference

## Technology Stack
- **Backend**: Django 5.0+, Python 3.12+
- **Frontend**: JavaScript, jQuery 3.7-slim
- **Maps**: Google Maps API, Mapbox API, Leaflet
- **Build**: Poetry for dependency management
- **Code Quality**: Black, isort, pre-commit hooks

## Installation & Setup
```bash
pip install django-map-widgets
```

Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    'mapwidgets',
]
```

## Configuration
Configure through `MAP_WIDGETS` setting in Django settings:
```python
MAP_WIDGETS = {
    "GoogleMap": {
        "apiKey": GOOGLE_MAP_API_KEY,
        "PointField": {
            "interactive": {
                "mapOptions": {"zoom": 15},
                "GooglePlaceAutocompleteOptions": {
                    "componentRestrictions": {"country": "uk"}
                },
            }
        }
    },
    "Mapbox": {
        "accessToken": MAPBOX_ACCESS_TOKEN,
        "PointField": {
            "interactive": {
                "mapOptions": {"zoom": 12},
                "markerFitZoom": 14,
            }
        },
    },
    "Leaflet": {
        "PointField": {
            "interactive": {
                "mapOptions": {"zoom": 12}
            }
        }
    }
}
```

## Usage Examples

### Django Admin
```python
from django.contrib.gis.db import models
import mapwidgets

class CityAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": mapwidgets.GoogleMapPointFieldWidget}
    }
```

### Django Forms
```python
from mapwidgets.widgets import GoogleMapPointFieldWidget

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ("coordinates",)
        widgets = {
            'coordinates': GoogleMapPointFieldWidget,
        }
```

## Development Environment
- **Package Version**: 0.5.1
- **Python**: 3.12+
- **Django**: 5.0.4+
- **Development Tools**: Black, isort, pre-commit, ipdb
- **Documentation**: Sphinx

## Future Roadmap
- Support for additional GeoDjango field types
- Enhanced customization options
- Performance optimizations
- Additional map provider integrations
- Mobile responsiveness improvements

## Links
- [GitHub Repository](https://github.com/erdem/django-map-widgets)
- [Documentation](http://django-map-widgets.readthedocs.io/)
- [PyPI Package](https://pypi.org/project/django-map-widgets/)
