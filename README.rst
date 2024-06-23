.. image:: https://badge.fury.io/py/django-map-widgets.svg
   :target: https://badge.fury.io/py/django-map-widgets

Django Map Widgets
==================

Django Map Widgets is a package that provides highly configurable, pluggable, and user-friendly map widgets for
GeoDjango form fields. It simplifies the integration of interactive maps into GeoDjango applications, enhancing the
overall development experience.

The primary goal of Django Map Widgets is to bridge the gap between powerful GeoDjango functionality and user-friendly
map interactions, creating a more accessible and enjoyable experience for both developers and end-users of
GeoDjango-powered applications.

.. image:: https://github.com/erdem/django-map-widgets/assets/1518272/61719dc4-244b-4f70-ba66-23985bb1233a
   :alt: Mapbox Interactive Widget



- `Documentation <http://django-map-widgets.readthedocs.io/>`_
- `Demo Project <https://github.com/erdem/django-map-widgets/tree/main/demo>`_
- `Home Page <https://github.com/erdem/django-map-widgets/>`_

Installation
~~~~~~~~~~~~

.. code-block:: shell

    pip install django-map-widgets

Add 'mapwidgets' to your ``INSTALLED_APPS`` in settings.py

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django.contrib.sessions',
        'django.contrib.staticfiles',

        'mapwidgets',
    ]

Ensure ``collectstatic`` Django admin command is run before using the widgets in production.

.. code-block:: shell

    python manage.py collectstatic

Usage
~~~~~

**Django Admin Usage**

.. code-block:: python

    from django.contrib.gis.db import models
    import mapwidgets


    class CityAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.PointField: {"widget": mapwidgets.GoogleMapPointFieldWidget}
        }

**Django Forms Usage**

.. code-block:: python

    from mapwidgets.widgets import GoogleMapPointFieldWidget, MapboxPointFieldWidget


    class CityForm(forms.ModelForm):
        class Meta:
            model = City
            fields = ("coordinates", "city_hall")
            widgets = {
                'coordinates': GoogleMapPointFieldWidget,
                'city_hall': MapboxPointFieldWidget,
            }

When the map widgets are used in Django web views with forms, Remember to include ``{{ form.media }}`` template tag in the
view templates.

Settings
~~~~~~~~

The JavaScript map rendering behavior of the widgets can be customized by providing ``MAP_WIDGETS`` config in the
project's settings file. For detailed guidance on map customization options, check
the `settings guide <http://django-map-widgets.readthedocs.io/settings>`_.

.. code-block:: python

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

JQuery Requirement
~~~~~~~~~~~~~~~~~~

jQuery is required for Django Map Widgets to function in regular Django views. However, if the widgets is being used
within the Django Admin, jQuery does not need to be provided separately. Any map widget class can be configured as
described in the documentation, and they will work out of the box.

Preferable jQuery version is ``3.7-slim``.

Support
~~~~~~~

Django Map Widgets offers two types of widgets:

1. **Interactive (Dynamic) Widgets**: These widgets allow users to interact with the map, such as clicking to set a
   location or dragging a marker. They are ideal for data input and editing scenarios.

2. **Static (Read-only) Widgets**: These widgets display map data in a non-interactive format. They are useful for
   presenting location information without allowing modifications.

**Widget Support Matrix**

+------------------------+-------------+--------+-------------+--------+-------------+--------+
| **GeoDjango Field**    | **GoogleMap**        | **Mapbox**          | **Leaflet**         |
+------------------------+-------------+--------+-------------+--------+-------------+--------+
|                        | Interactive | Static | Interactive | Static | Interactive | Static |
+========================+=============+========+=============+========+=============+========+
| *PointField*           | ✅           | ✅      | ✅           | ✅      | ✅           | N/A    |
+------------------------+-------------+--------+-------------+--------+-------------+--------+
| *LineStringField*      | ✖️          | ✖️     | ✖️          | ✖️     | ✖️          | N/A    |
+------------------------+-------------+--------+-------------+--------+-------------+--------+
| *PolygonField*         | ✖️          | ✖️     | ✖️          | ✖️     | ✖️          | N/A    |
+------------------------+-------------+--------+-------------+--------+-------------+--------+
| *MultiPointField*      | ✖️          | ✖️     | ✖️          | ✖️     | ✖️          | N/A    |
+------------------------+-------------+--------+-------------+--------+-------------+--------+
| *MultiLineStringField* | ✖️          | ✖️     | ✖️          | ✖️     | ✖️          | N/A    |
+------------------------+-------------+--------+-------------+--------+-------------+--------+
| *MultiPolygonField*    | ✖️          | ✖️     | ✖️          | ✖️     | ✖️          | N/A    |
+------------------------+-------------+--------+-------------+--------+-------------+--------+

Contribution
~~~~~~~~~~~~

Currently, the package supports Google, Mapbox, and Leaflet mapping platforms. If you have ideas for additional map
providers or new features, or even if you want to help extend support to other GeoDjango form fields, feel free to do
so. We would be happy to review and merge your contributions.

For more info how to contribute, please check out
the `contribution guidelines <http://django-map-widgets.readthedocs.io/contribution>`_.

Screenshots
~~~~~~~~~~~

MapBox Interactive Point Field Widget
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: https://github.com/erdem/django-map-widgets/assets/1518272/78332233-c4eb-4469-a751-69a9f06e0c8b
   :alt: MapBox Interactive Point Field Widget

MapBox Static Point Field Widget
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: https://github.com/erdem/django-map-widgets/assets/1518272/f53079c0-cd2a-4115-ba11-c74c82bca890
   :alt: MapBox Static Point Field Widget

GoogleMap Interactive Point Field Widget
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: https://github.com/erdem/django-map-widgets/assets/1518272/6b779cf1-b758-4917-9c4a-82db9605a88f
   :alt: GoogleMap Interactive Point Field Widget

Leaflet Interactive Point Field Widget
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: https://github.com/erdem/django-map-widgets/assets/1518272/2da338aa-a280-4fd3-ae33-bc9e8ffe3b2c
   :alt: Leaflet Interactive Point Field Widget

and more...