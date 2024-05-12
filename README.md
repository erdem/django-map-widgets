[![Coverage Status](https://coveralls.io/repos/github/erdem/django-map-widgets/badge.svg?branch=master)](https://coveralls.io/github/erdem/django-map-widgets?branch=master)
[![Build Status](https://travis-ci.org/erdem/django-map-widgets.png)](https://travis-ci.org/erdem/django-map-widgets)
[![PyPI version](https://badge.fury.io/py/django-map-widgets.svg)](https://badge.fury.io/py/django-map-widgets)

## Django Map Widgets

Django Map Widgets is a Python package that provides configurable, pluggable, and user-friendly map widgets for Django
PostGIS fields.

* [Documentation](http://django-map-widgets.readthedocs.io/)
* [Home Page](https://github.com/erdem/django-map-widgets/)
* [Demo Project](https://github.com/erdem/django-map-widgets/tree/master/demo)

### Achievements

The goal of the Django Map Widgets package is to create user-friendly UI widgets for GeoDjango form fields that are
highly configurable.

Currently, the package supports Google, Mapbox, and Leaflet map providers. If you would like to see support for
additional providers and believe you can contribute, feel free to do so. We would be happy to review and merge your
contributions.

For more info how to contribute, please check out the contribution guideline.

### Installation

    pip install django-map-widgets

Add ‘mapwidgets’ to your `INSTALLED_APPS` in settings.py

```python
INSTALLED_APPS = [
    ...
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'mapwidgets',
]

```

Run `collectstatic` django admin command before use the widgets

```shell
python manage.py collectstatic
```

### Usages

**Django Admin Usage**

```python
from django.contrib.gis.db import models
import mapwidgets


class CityAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": mapwidgets.GoogleMapPointFieldWidget}
    }
```

**Django Forms Usage**

```python
from mapwidgets.widgets import GoogleMapPointFieldWidget, MapboxPointFieldWidget


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ("coordinates", "city_hall")
        widgets = {
            'coordinates': GoogleMapPointFieldWidget,
            'city_hall': MapboxPointFieldWidget,
        }
```

...and your template should look something like this

```html

<form method="POST" action="">
    {% csrf_token %}
    {{form.media}}
    {{form.as_p}}
</form>
```

The JavaScript map rendering behavior of the widgets can be customized by providing `MAP_WIDGETS` config in your Django
project's settings file. For detailed guidance on map customization options, check the settings guide.

**Example Settings**

```python
GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")
MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")

MAP_WIDGETS = {
    "GoogleMap": {
        "apiKey": GOOGLE_MAP_API_KEY,
        "PointField": {
            "interactive": {
                "mapOptions": {
                    "zoom": 15,  # set initial zoom
                    "streetViewControl": False,
                },
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
                "mapOptions": {"zoom": 12, "center": (51.515618, -0.091998)},
                "markerFitZoom": 14,
            }
        },
    },
    "Leaflet": {
        "PointField": {
            "interactive": {
                "mapOptions": {
                    "zoom": 12,
                    "scrollWheelZoom": False
                }
            }
        },
        "markerFitZoom": 14,
    }
}
```

### Javascript Requirements

Django Map Widgets requires jQuery to function in your regular Django views. However, if you are using the widget within
the Django Admin, you do not need to provide jQuery separately. You can simply configure any map widget class as
described in the documentation, and they will work out of the box.

### Screenshots

##### GoogleMap Interactive Point Field Widget

![](https://cloud.githubusercontent.com/assets/1518272/26807500/ad0af4ea-4a4e-11e7-87d6-632f39e438f7.gif)

##### MapBox Interactive Point Field Widget

![](https://user-images.githubusercontent.com/1518272/168497515-f97363f4-6860-410e-9e24-230a2c4233b7.png)

### Release Notes

#### 0.4.2

> - GooglePointFieldInlineWidget bug fixes for Django 4.2.x (#142), thanks for @isarota.
> - Added `.readthedocs.yaml` to cover new **Read the Docs** updates.

#### 0.4.1

> - Added scroll wheel zooming functionality switch to Google Point Map Settings. (#134)
> - Added Chinese(ZH) localisation support. (#133)

#### 0.4.0

> - Supported MapBox Map for Django Geo Point Field.
> - Fixed undefined place object binding issue in javascript triggers. (#125)
> - Documented MapBox point field map widget features.
> - Updated various localize files.


[See release notes](https://django-map-widgets.readthedocs.io/en/mapbox_widget_fixes/releases/index.html) for all
versions.