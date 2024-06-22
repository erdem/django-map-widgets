.. _contribution:


============
Contribution
============

The journey of this project began in 2016 at a local hackathon event. The initial goal was to create a user-friendly interface for GeoDjango PointField inputs. Since its inception, the project has undergone numerous changes, with new widgets added for various providers and it has become a dependency for many global projects.

The current vision of the project is to develop user-friendly and developer-friendly interfaces for all GeoDjango field types using major JavaScript-based map services. If your projects require a widget that is not yet supported by django-map-widgets, you can follow this guide to contribute new widgets to the project.


Demo Project Setup
------------------
The `demo project <https://github.com/erdem/django-map-widgets/tree/master/demo>`_ is a convenient development environment for creating various types of widgets. You can find many examples of existing widgets being used in the admin interface and views.

.. image:: /_static/images/demo_project_preview.png

To run the project, a PostgreSQL database with the PostGIS plugin is required. Follow the instructions in the `Django Installing PostGIS Documentation <https://docs.djangoproject.com/en/5.0/ref/contrib/gis/install/postgis/#post-installation>`_ to create a database with PostGIS. Update the project's ``DATABASES`` configuration in ``demo/settings.py`` if necessary.

Create and configure the database:

.. code-block:: psql

    createdb djmap_demo
    psql djmap_demo
    CREATE EXTENSION postgis;

.. code-block:: python

    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": "djmap_demo",
            "USER": "",
            "PASSWORD": "",
            "HOST": "localhost",
        }
    }

Apply database migrations:

.. code-block:: shell

    python manage.py migrate

Set environment variables:

.. list-table::
   :header-rows: 1

   * - Name
     - Description
   * - GOOGLE_MAP_API_KEY
     - Required for GoogleMap interactive widgets.
   * - GOOGLE_MAP_API_SECRET
     - Required for GoogleMap static widgets.
   * - MAPBOX_ACCESS_TOKEN
     - Required for Mapbox interactive widgets.
   * - MAPBOX_ACCESS_USERNAME
     - Set this if Mapbox static map images will use a custom user map style; otherwise, it can be left as is.

Run the development server and start exploring the project at `http://localhost:8000/ <http://localhost:8000/>`_:

.. code-block:: shell

    python manage.py runserver 0:8000


