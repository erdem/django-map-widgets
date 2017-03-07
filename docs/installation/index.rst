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

Requirements
^^^^^^^^^^^^

Django map widgets uses the inbuilt django jQuery library. No further admin settings is required.

