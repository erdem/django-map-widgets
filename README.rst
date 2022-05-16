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

.. note::
    Please check the `project home page <https://github.com/erdem/django-map-widgets/>`_ for latest updates.

 * **Project Home Page** : `https://github.com/erdem/django-map-widgets <https://github.com/erdem/django-map-widgets/>`_.
 * **Documentation**:  `http://django-map-widgets.readthedocs.io <http://django-map-widgets.readthedocs.io/>`_.

Achievements
^^^^^^^^^^^^

| The aim of the Django map widgets is to make all Geo Django widgets more user-friendly and configurable.  
|   
| Django map widgets package has support for Mapbox and Google Map services currently, if you want to see more widgets and think you can help, feel free to contribute to the project. 
| We would be happy to review and merge your contributions. :) 

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

=====
0.4.0
=====

 * Supported MapBox Map for Geo Point Field
 * Fixed undefined place object binding issue in javascript triggers. (#125)
 * Documented MapBox point field map widget
 * Updated various localize files.


======
v0.3.2
======

 * Added `streetViewControl <https://developers.google.com/maps/documentation/javascript/streetview#StreetViewMapUsage>`_ switch option to GooglePointFieldWidget settings. (#124)

======
v0.3.1
======

 * Removed `six` package usages. (#117)
 * Added a new general widget setting in order to specify Google JS libraries. (#119)
 * Implemented some improvements for the demo project.

======
v0.3.0
======

 * Implemented a new demo project with Django 2.x.
 * Fixed Django Admin jQuery conflicts. (#100)
 * Fixed a new widget JS instance initialising issue for Django Admin Inlines. (#84)
 * Added Python 3.8 env settings to TravisCI configuration.
