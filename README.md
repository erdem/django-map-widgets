[![Coverage Status](https://coveralls.io/repos/github/erdem/django-map-widgets/badge.svg?branch=master)](https://coveralls.io/github/erdem/django-map-widgets?branch=master)
[![Build Status](https://travis-ci.org/erdem/django-map-widgets.png)](https://travis-ci.org/erdem/django-map-widgets)
[![PyPI version](https://badge.fury.io/py/django-map-widgets.svg)](https://badge.fury.io/py/django-map-widgets)

### Django Map Widgets
Configurable, pluggable and more user friendly map widgets for Django PostGIS fields.

* **Documentation**: <a href="http://django-map-widgets.readthedocs.io/" target="_blank">http://django-map-widgets.readthedocs.io/</a>
* **Project Home Page**: <a href="https://github.com/erdem/django-map-widgets">https://github.com/erdem/django-map-widgets/</a>

### Achievements
The aim of the Django map widgets is to make all Geo Django widgets more user-friendly and configurable.  
  
Django map widgets package has support for Mapbox and Google Map services currently, if you want to see more widgets and think you can help, feel free to contribute to the project.  
We would be happy to review and merge your contributions. :) 

### Installation

    pip install django-map-widgets


Add ‘map_widgets’ to your `INSTALLED_APPS` in settings.py

```python
INSTALLED_APPS = [
     ...
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mapwidgets',
]
```

Collects the static files into `STATIC_ROOT`.

```bash
python manage.py collectstatic
```

**Django Admin**

```python
from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget


class CityAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
```

**Django Forms**

```python
from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticOverlayMapWidget


class CityForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ("coordinates", "city_hall")
        widgets = {
            'coordinates': GooglePointFieldWidget,
            'city_hall': GoogleStaticOverlayMapWidget,
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

### Requirements

Django Map Widgets needs Jquery dependency to work in your regular views. In Django Admin case, you don't need to provide the jQuery. 
Just add map widgets to your django admin forms. 

### Screenshots

##### Google Map Point Field Widget

![](https://cloud.githubusercontent.com/assets/1518272/26807500/ad0af4ea-4a4e-11e7-87d6-632f39e438f7.gif)


##### MapBox Map Point Field Widget

![](https://user-images.githubusercontent.com/1518272/168497515-f97363f4-6860-410e-9e24-230a2c4233b7.png)


##### Google Map Static Overlay Widget
This widget is working with <a href="http://dimsemenov.com/plugins/magnific-popup/" target="_blank">Magnific Popup</a> jQuery plugin.

![](https://cloud.githubusercontent.com/assets/1518272/18732296/18f1813e-805a-11e6-8801-f1f48ed02a9c.png)


### Release Notes

#### 0.4.0
> -   Supported MapBox Map for Django Geo Point Field.
> -   Fixed undefined place object binding issue in javascript triggers. (#125)
> -   Documented MapBox point field map widget features.
> -   Updated various localize files.

#### 0.3.3

> -   Replaced [ugettext_lazy](https://github.com/erdem/django-map-widgets/pull/127) usages with [gettext_lazy](https://docs.djangoproject.com/en/4.0/releases/4.0/#features-removed-in-4-0) for Django 4.0. (#127)
> -   Updated [Travis CI file](https://github.com/erdem/django-map-widgets/pull/129). (#129)

#### 0.3.2

> -   Added [streetViewControl](https://developers.google.com/maps/documentation/javascript/streetview#StreetViewMapUsage) switch to GooglePointFieldWidget settings. (#124)

#### 0.3.1

> -   Removed `six` package usages. (#117)
> -   Added a new general widget setting in order to specify Google JS libraries. (#119)
> -   Implemented some improvements for the demo project.

#### 0.3.0

> -   Implemented a new demo project with Django 2.x.
> -   Fixed Django Admin jQuery conflicts. (#100)
> -   Fixed a new widget JS instance initialising issue for Django Admin Inlines. (#84)
> -   Added Python 3.8 env settings to TravisCI configuration.

[See release notes](https://django-map-widgets.readthedocs.io/en/mapbox_widget_fixes/releases/index.html) for all versions.