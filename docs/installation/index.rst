Installation
------------
.. note:: The library has been tested against Python 2.7 and 3.4+.


Installing from PyPi
^^^^^^^^^^^^^^^^^^^^
.. note:: This is the preferred installation method.

.. code-block:: console

    $ pip install django-map-widgets


Installing from source
^^^^^^^^^^^^^^^^^^^^^^
Alternatively, install the package from github

.. code-block:: console

    $ pip install git+git://github.com/erdem/django-map-widgets.git


Add ‘map_widgets’ to your `INSTALLED_APPS` in settings.py


.. code-block:: python

    INSTALLED_APPS = [
         ...
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'mapwidgets',
    ]

Collects the static files into ``STATIC_ROOT``.

.. code-block:: bash
    
    python manage.py collectstatic


If you are using ``mapwidgets`` in your regular django views, you need to add ``{{ form.media }}`` template variable to the ``<head>`` or end of the ``<body>`` HTML section of your templates:

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
      ...
      {{ form.media }}
    </head>
    <body>
    ...
    </body>
    </html>


.. note:: If you are using ``mapwidgets`` on the Django Admin, you don't need to add ``{{ form.media }}`` any template files. The media variable already added in default Django Admin templates.

Requirements
^^^^^^^^^^^^

Django Map Widgets needs Jquery dependency to work in your regular views. In Django Admin case, you don't need to provide the jQuery just because it's already available on ``django.jQuery`` namespace.

