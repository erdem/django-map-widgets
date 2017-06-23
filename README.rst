.. image:: https://coveralls.io/repos/github/erdem/django-map-widgets/badge.svg?branch=master
    :target: https://coveralls.io/github/erdem/django-map-widgets?branch=master
    :alt: Coverage Status

.. image:: https://travis-ci.org/erdem/django-map-widgets.png
    :target: https://travis-ci.org/erdem/django-map-widgets
    :alt: Build Status

.. image:: https://badge.fury.io/py/django-map-widgets.svg
    :target: https://badge.fury.io/py/django-map-widgets
    :alt: Latest PyPI version

Django Map Widgets
==================

Configurable, pluggable and more user friendly map widgets for Django PostGIS fields.

 * **Documentation**:  `http://django-map-widgets.readthedocs.io <http://django-map-widgets.readthedocs.io/>`_.
 * **Project Home Page** : `https://github.com/erdem/django-map-widgets <https://github.com/erdem/django-map-widgets/>`_.

Achievements
^^^^^^^^^^^^

The aim of the Django map widgets is to make all Geo Django widgets more user friendly and configurable. Map widgets support major map services (GoogleMaps, OpenStreetMap) for your geoDjango fields.


Installation
^^^^^^^^^^^^

.. code-block:: console

    $ pip install django-map-widgets

Add ``map_widgets`` to your ``INSTALLED_APPS`` in settings.py

.. code-block:: python

    INSTALLED_APPS = [
         ...
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'mapwidgets',
    ]

**Django Admin**

.. code-block:: python
    from django.contrib.gis.db import models
    from mapwidgets.widgets import GooglePointFieldWidget


    class CityAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.PointField: {"widget": GooglePointFieldWidget}
        }


**Django Forms**

.. code-block:: python

    from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticOverlayMapWidget


    class CityForm(forms.ModelForm):

        class Meta:
            model = City
            fields = ("coordinates", "city_hall")
            widgets = {
                'coordinates': GooglePointFieldWidget,
                'city_hall': GoogleStaticOverlayMapWidget,
            }


Requirements
^^^^^^^^^^^^

Django Map Widgets needs Jquery dependency to work in your regular views. In Django Admin case, you don't need to provide the jQuery just because it's already available on ``django.jQuery`` namespace.

Screenshots
^^^^^^^^^^^

Google Map Point Field Widget
-----------------------------

.. image:: https://cloud.githubusercontent.com/assets/1518272/26807500/ad0af4ea-4a4e-11e7-87d6-632f39e438f7.gif
   :width: 100 %


Google Map Static Overlay Widget
--------------------------------

.. image:: https://cloud.githubusercontent.com/assets/1518272/18732296/18f1813e-805a-11e6-8801-f1f48ed02a9c.png
   :width: 100 %


Release Notes
^^^^^^^^^^^^^

======
v0.1.9
======

 * Google Place Autocomplete object binding to jQuery triggers.
 * Implemented Google Geocoding support for the marker coordinates.
 * Added custom widget settings feature for each widget.
 * Added Portuguese localisation support.
 * Fixed Google Place Autocomplete widget bugs in Django Admin Inlines.
 * Fixed Python 3.6 errors.
 * Fixed Javascript bugs.
 * The GitHub repository Integrated with Travis CI.
 * Implemented unit tests for backend code. (%100 code coverage)
 * Change development environment from Vagrant to Docker.

======
v0.1.8
======

 * Full documentation integrated to readthedocs.org.
 * Fixed Google Map static widget issues.
 * Added Russian localisation support.
 * Added `Google Places Autocomplete <https://developers.google.com/maps/documentation/javascript/places-autocomplete>`_ options support.
 * Fixed CSS issues.
