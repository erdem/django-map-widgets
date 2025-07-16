# Django Map Widgets - LLM Code Style Guide

## Code Style Guidelines

### Python Code Standards
- **Formatter**: Black (target Python 3.11+)
- **Import Sorting**: isort with black profile
- **Line Length**: 88 characters (Black default)
- **Pre-commit**: Enabled with hooks for black, isort

### Django Conventions
- Follow Django's coding style guidelines
- Use Django's built-in features and patterns
- Prefer Django's class-based views and forms
- Use Django's translation framework for internationalization

### Widget Development Patterns

#### Base Widget Structure
```python
class BaseWidget(forms.Widget):
    template_name = 'path/to/template.html'
    
    class Media:
        css = {'all': ('path/to/styles.css',)}
        js = ('path/to/script.js',)
    
    def __init__(self, attrs=None, **kwargs):
        super().__init__(attrs)
        # Widget-specific initialization
    
    def format_value(self, value):
        # Handle value formatting
        pass
    
    def get_context(self, name, value, attrs):
        # Build template context
        context = super().get_context(name, value, attrs)
        # Add widget-specific context
        return context
```

#### Mixin Usage
- Use mixins for shared functionality across widgets
- Keep mixins focused and single-purpose
- Document mixin dependencies and requirements

#### Configuration Handling
```python
from django.conf import settings
from .settings import MAP_WIDGETS_SETTINGS

def get_widget_config(provider, field_type, widget_type):
    """Get configuration for specific widget."""
    config = MAP_WIDGETS_SETTINGS.get(provider, {})
    return config.get(field_type, {}).get(widget_type, {})
```

### JavaScript/Frontend Standards

#### JavaScript Structure
- Use ES5 syntax for broad compatibility
- Wrap code in immediately invoked function expressions (IIFE)
- Use strict mode
- Handle jQuery dependency gracefully

```javascript
(function($) {
    'use strict';
    
    // Widget implementation
    
})(django.jQuery || jQuery);
```

#### Map Provider Integration
- Abstract common map operations
- Handle API key/token validation
- Provide fallback for missing dependencies
- Implement error handling for API failures

### File Organization

#### Widget Files
```
mapwidgets/
├── widgets/
│   ├── __init__.py          # Widget exports
│   ├── base.py              # Base classes and mixins
│   ├── googlemap.py         # Google Maps widgets
│   ├── mapbox.py            # Mapbox widgets
│   ├── leaflet.py           # Leaflet widgets
│   └── mixins.py            # Shared mixins
├── static/mapwidgets/
│   ├── css/                 # Widget stylesheets
│   ├── js/                  # Widget JavaScript
│   └── images/              # Widget images
└── templates/mapwidgets/    # Widget templates
```

#### Template Structure
```html
<!-- templates/mapwidgets/widget_name.html -->
<div class="map-widget" data-widget-type="{{ widget_type }}">
    {{ widget.render }}
</div>
```

### Testing Guidelines

#### Unit Tests
```python
from django.test import TestCase
from django.forms import Form
from .widgets import GoogleMapPointFieldWidget

class GoogleMapWidgetTest(TestCase):
    def test_widget_initialization(self):
        widget = GoogleMapPointFieldWidget()
        self.assertIsNotNone(widget)
    
    def test_widget_render(self):
        widget = GoogleMapPointFieldWidget()
        html = widget.render('location', None)
        self.assertIn('map-widget', html)
```

#### Integration Tests
- Test widget rendering in forms
- Test JavaScript functionality
- Test configuration handling
- Test error scenarios

### Documentation Standards

#### Docstrings
```python
def widget_method(self, param):
    """Brief description of method.
    
    Args:
        param (type): Description of parameter.
    
    Returns:
        type: Description of return value.
    
    Raises:
        ExceptionType: Description of when exception is raised.
    """
```

#### Comments
- Use comments sparingly for complex logic
- Prefer self-documenting code
- Comment why, not what
- Keep comments up-to-date with code changes

### Performance Considerations

#### Static Files
- Minimize and compress JavaScript/CSS for production
- Use Django's static file handling
- Implement lazy loading for map libraries
- Cache widget configurations

#### Database
- Optimize GeoDjango queries
- Use appropriate spatial indexes
- Consider pagination for large datasets

### Error Handling

#### Python Exceptions
```python
try:
    # Widget operation
    pass
except ImportError:
    raise ImproperlyConfigured(
        "Map provider library not installed. "
        "Please install the required dependencies."
    )
except Exception as e:
    logger.error(f"Widget error: {e}")
    # Provide fallback or re-raise
```

#### JavaScript Errors
```javascript
try {
    // Map operation
} catch (error) {
    console.error('Map widget error:', error);
    // Provide user-friendly fallback
}
```

### Security Considerations

#### API Keys
- Never expose API keys in client-side code
- Use environment variables for sensitive data
- Implement proper key rotation procedures
- Validate API key formats

#### Input Validation
- Sanitize all user inputs
- Validate coordinate ranges
- Protect against XSS attacks
- Use Django's built-in security features

### Accessibility Guidelines

#### HTML Structure
- Use semantic HTML elements
- Provide proper ARIA labels
- Ensure keyboard navigation support
- Include alternative text for images

#### CSS
- Ensure sufficient color contrast
- Support high contrast modes
- Provide focus indicators
- Support screen readers

### Versioning and Compatibility

#### Python/Django Support
- Support actively maintained Python versions
- Follow Django's LTS release schedule
- Test against multiple Django versions
- Document version compatibility

#### Browser Support
- Support modern browsers (last 2 versions)
- Provide graceful degradation
- Test on mobile devices
- Document browser requirements

### Contribution Guidelines

#### Code Reviews
- All changes require review
- Test coverage should not decrease
- Documentation must be updated
- Follow established patterns

#### Commit Messages
```
feat(widgets): add support for Leaflet static widgets

- Implement LeafletPointFieldStaticWidget
- Add corresponding JavaScript handlers
- Update documentation and examples
- Add unit tests for new widget

Fixes #123
```

#### Pull Request Process
1. Create feature branch from main
2. Implement changes with tests
3. Update documentation
4. Submit PR with clear description
5. Address review feedback
6. Merge after approval

This style guide ensures consistency across the codebase and provides clear guidelines for contributors and LLM assistants working on the project.
