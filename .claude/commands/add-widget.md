# /add-widget — Add a new map widget

Scaffold a new map widget across all required files (Python, JS, CSS, templates, docs).

## What it does
Interactively prompts for widget details, then generates:
1. **Python widget class** in `mapwidgets/widgets/<provider>.py`
   - Extends `BasePointFieldInteractiveWidget` or `BaseStaticWidget`
   - Registers in widget's `__init__.py` and main `__init__.py`

2. **Settings** in `mapwidgets/settings.py`
   - Adds provider config to `DEFAULT_SETTINGS`
   - Includes apiKey, mapOptions, media paths

3. **JavaScript** in `mapwidgets/static/mapwidgets/js/pointfield/interactive/<provider>/`
   - Creates `mw_pointfield.js` (unminified)
   - Runs `/minify` to generate `.min.js`

4. **CSS** in `mapwidgets/static/mapwidgets/css/` (if needed)

5. **HTML template** in `mapwidgets/templates/mapwidgets/`
   - Django form widget template

6. **Documentation** stub in `docs/widgets/`
   - Includes provider name, installation, configuration, usage examples

## Usage
```
/add-widget
```

Prompts you for:
- **Provider name** (e.g., "Google Maps", "Mapbox", "Leaflet")
- **Widget types** to create (interactive, static, inline formsets)
- **API/auth requirements** (apiKey, token, etc.)

## Follow-up
After running, you should:
- Update widget JS logic for your specific provider
- Test widget rendering in demo project
- Run `/minify` if JS was modified
- Commit changes with meaningful message

## Reference
See `docs/contribution/index.rst` for the full new widget checklist.
