# Google Places API Migration Guide

## Overview

Google has deprecated the `google.maps.places.Autocomplete` class in favor of the new `google.maps.places.PlaceAutocompleteElement`. As of March 1st, 2025, google.maps.places.Autocomplete is not available to new customers, and existing users should migrate to ensure continued support.

## What Changed

### Legacy API (Deprecated)
```javascript
// Old way - being deprecated
const autocomplete = new google.maps.places.Autocomplete(inputElement, options);
autocomplete.addListener('place_changed', handler);
```

### New API (Recommended)
```javascript
// New way - recommended
const placeAutocomplete = new google.maps.places.PlaceAutocompleteElement(options);
placeAutocomplete.addEventListener('gmp-select', async (event) => {
    const place = event.placePrediction.toPlace();
    await place.fetchFields({ fields: ['displayName', 'formattedAddress', 'location'] });
});
```

## Django Map Widgets Migration

Django Map Widgets now supports **both APIs** with automatic detection and fallback. The widget will:

1. **Auto-detect** which API is available
2. **Prefer the new API** when available
3. **Fallback to legacy** if the new API is not supported
4. **Allow manual override** through settings

## Configuration Options

### Automatic Migration (Recommended)

No changes needed! The widget automatically detects and uses the appropriate API:

```python
# settings.py - No changes required for auto-migration
MAP_WIDGETS = {
    "GoogleMap": {
        "apiKey": "your-api-key",
        "PointField": {
            "interactive": {
                "GooglePlaceAutocompleteOptions": {
                    "componentRestrictions": {"country": "us"}
                }
            }
        }
    }
}
```

### Manual Control

You can explicitly control which API to use:

```python
# settings.py
MAP_WIDGETS = {
    "GoogleMap": {
        "apiKey": "your-api-key", 
        "PointField": {
            "interactive": {
                # Control which Places API to use
                "useNewPlacesAPI": "auto",  # "auto", "legacy", "new"
                
                # Auto-fallback when new API fails
                "autoFallbackToLegacy": True,
                
                "GooglePlaceAutocompleteOptions": {
                    "componentRestrictions": {"country": "us"},
                    "types": ["address"]
                }
            }
        }
    }
}
```

#### Configuration Values

- **`"auto"`** (default): Automatically detect and use the best available API
- **`"new"`**: Force use of new PlaceAutocompleteElement API
- **`"legacy"`**: Force use of legacy Autocomplete API
- **`autoFallbackToLegacy`**: Whether to fallback to legacy API if new API fails

## Option Mapping

The widget automatically maps legacy options to the new API:

| Legacy Option | New API Equivalent | Notes |
|---------------|-------------------|-------|
| `componentRestrictions.country` | `includedRegionCodes` | Array of country codes |
| `types` | `includedPrimaryTypes` | Place types filter |
| `bounds` | `locationBias` | Geographic bounds |
| Input element styling | Automatic | CSS classes copied to new element |

## Compatibility

### Supported Features

✅ **Country restrictions** - Automatically mapped  
✅ **Place types filtering** - Automatically mapped  
✅ **Bounds/location bias** - Automatically applied  
✅ **Placeholder text** - Preserved from original input  
✅ **CSS styling** - Applied to new element  
✅ **Event handling** - Unified interface for both APIs  
✅ **Error handling** - Graceful fallback to legacy API  

### Behavior Changes

- **Input Element**: New API creates its own input element instead of using existing one
- **Event Names**: Uses `gmp-select` instead of `place_changed` (handled internally)
- **Place Object**: New API returns different place object structure (converted automatically)

## Testing Your Migration

### 1. Test Auto-Detection

```javascript
// Check if new API is being used
console.log('Using new Places API:', window.google?.maps?.places?.PlaceAutocompleteElement !== undefined);
```

### 2. Force New API

```python
# Test with new API only
MAP_WIDGETS = {
    "GoogleMap": {
        "PointField": {
            "interactive": {
                "useNewPlacesAPI": "new",
                "autoFallbackToLegacy": False
            }
        }
    }
}
```

### 3. Force Legacy API

```python
# Test with legacy API only  
MAP_WIDGETS = {
    "GoogleMap": {
        "PointField": {
            "interactive": {
                "useNewPlacesAPI": "legacy"
            }
        }
    }
}
```

## Troubleshooting

### Common Issues

**Issue**: New autocomplete element not appearing  
**Solution**: Check browser console for errors, ensure API key has Places API enabled

**Issue**: Styling looks different  
**Solution**: CSS classes are automatically copied, but you may need to update custom styles

**Issue**: Country restrictions not working  
**Solution**: Ensure country codes are in ISO 3166-1 Alpha-2 format (e.g., "us", "gb")

### Debugging

Enable debug logging:

```javascript
// Check which API is being used
console.log('Widget settings:', widgetSettings);
console.log('Using new API:', widget.placeAutocompleteElement !== undefined);
console.log('Using legacy API:', widget.autocomplete !== undefined);
```

## API Key Requirements

Ensure your Google Maps API key has the following APIs enabled:

- **Maps JavaScript API** (required)
- **Places API** (required for autocomplete functionality)

## Browser Support

- **New API**: Modern browsers supporting Web Components
- **Legacy API**: Broader browser support including older versions
- **Auto-detection**: Works in all supported browsers

## Migration Timeline

- **Before March 1, 2025**: Both APIs available
- **After March 1, 2025**: New customers can only use new API
- **Legacy users**: Can continue using legacy API with 12 months notice before discontinuation

## Support

If you encounter issues:

1. Check the browser console for error messages
2. Verify your API key has the required permissions
3. Test with `useNewPlacesAPI: "legacy"` to isolate new API issues
4. Report issues on the [GitHub repository](https://github.com/erdem/django-map-widgets/issues)

## Example Implementation

Here's a complete example showing both manual and automatic migration:

```python
# settings.py
GOOGLE_MAP_API_KEY = "your-api-key"

MAP_WIDGETS = {
    "GoogleMap": {
        "apiKey": GOOGLE_MAP_API_KEY,
        "PointField": {
            "interactive": {
                # Automatic migration (recommended)
                "useNewPlacesAPI": "auto",
                "autoFallbackToLegacy": True,
                
                # Your existing options work unchanged
                "mapOptions": {"zoom": 15},
                "GooglePlaceAutocompleteOptions": {
                    "componentRestrictions": {"country": ["us", "ca"]},
                    "types": ["address"]
                }
            }
        }
    }
}
```

```python
# forms.py - No changes needed!
from mapwidgets.widgets import GoogleMapPointFieldWidget

class LocationForm(forms.Form):
    location = forms.PointField(
        widget=GoogleMapPointFieldWidget
    )
```

The migration is designed to be **seamless and backward-compatible**. Your existing code will continue to work while automatically benefiting from the new API when available.
