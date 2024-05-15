Django Map Widgets supports Django 4.x-5.x and Python 3.9+.

Installation
============

1. Install the package:

.. code-block:: shell

    pip install django-map-widgets

2. Add mapwidgets to your INSTALLED_APPS in settings.py:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django.contrib.sessions',
        'django.contrib.staticfiles',

        'mapwidgets',
    ]

3. Run the `collectstatic` command to ensure static files are correctly collected before using the widgets in production:

.. code-block:: shell

    python manage.py collectstatic

Getting Started
===============

All widgets can initialize with GeoDjango form fields like any other Django widgets.

**Javascript Requirements**


jQuery is required for Django Map Widgets to function in regular Django views. However, if the widgets are used within the Django Admin, jQuery does not need to be provided separately (it uses django admin jQuery to function). Any map widget class can be configured as described in the documentation, and they will work out of the box.

The preferable jQuery version is 3.x-slim.

Usage
-----

**Django Admin Usage Example**

.. code-block:: python

    from django.contrib.gis.db import models
    import mapwidgets


    class CityAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.PointField: {"widget": mapwidgets.GoogleMapPointFieldWidget}
        }

** Django Forms Usage Example**


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


When using map widgets in Django views, include `{{ form.media }}` template variable in the <head> or at the end of the <body> tag in django templates:

.. code-block:: html

    <html>
    <head>
        <title>...</title>
        {{ form.media }}
    </head>
    <body>
        ....
        <form method="POST" action="">
            {% csrf_token %}
            {{form.as_p}}
        </form>
    </body>
    </html>

Configuration
-------------

The JavaScript map rendering behavior of the widgets can be customized by providing `MAP_WIDGETS` configuration in your project's settings file. For detailed guidance on map customization options, refer to the `settings guide <http://django-map-widgets.readthedocs.io/settings>`_.

**Example Settings**

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



Screenshots
-----------

**GoogleMap Interactive Point Field Widget**


.. image:: https://cloud.githubusercontent.com/assets/1518272/26807500/ad0af4ea-4a4e-11e7-87d6-632f39e438f7.gif
   :alt: GoogleMap Interactive Point Field Widget

**MapBox Interactive Point Field Widget**

.. image:: https://user-images.githubusercontent.com/1518272/168497515-f97363f4-6860-410e-9e24-230a2c4233b7.png
   :alt: MapBox Interactive Point Field Widget
