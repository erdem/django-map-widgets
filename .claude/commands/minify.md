# /minify — Minify JS & CSS assets

Minify all JavaScript and CSS files in the mapwidgets static assets using the build script.

## What it does
- Runs `python scripts.py` to minify JS files in `mapwidgets/static/mapwidgets/js/`
- Minifies CSS in `mapwidgets/static/mapwidgets/css/`
- Generates `.min.js` and `.min.css` files
- Verifies all minified assets were created successfully

## Usage
```
/minify
```

## When to use
- After creating a new widget JS file
- After modifying any `.js` or `.css` files in `mapwidgets/static/`
- Before committing changes to static assets
- As part of the release process
