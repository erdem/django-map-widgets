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

Add ‘map_widgets’ to your `INSTALLED_APPS` in settings.py

.. code-block:: python

    INSTALLED_APPS = [
         ...
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'mapwidgets',
    ]


Requirements
^^^^^^^^^^^^

Django Map Widgets needs Jquery dependency to work in your regular views. In Django Admin case, you don't need to provide the jQuery just because it's already available on ``django.jQuery`` namespace.

Screenshots
^^^^^^^^^^^

Google Map Point Field Widget
-----------------------------

.. image:: https://cloud.githubusercontent.com/assets/1518272/18732352/724dd098-805a-11e6-8eb4-6ba9b5e06a81.png
   :width: 100 %


Google Map Point Field Widget for Django Admin Inlines
------------------------------------------------------

.. image:: https://cloud.githubusercontent.com/assets/1518272/18221609/2cac10fe-7178-11e6-9990-a93176693ef7.gif

Google Map Static Overlay Widget
--------------------------------

.. image:: https://cloud.githubusercontent.com/assets/1518272/18732296/18f1813e-805a-11e6-8801-f1f48ed02a9c.png
   :width: 100 %

