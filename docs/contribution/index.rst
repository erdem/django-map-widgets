.. _contribution:


============
Contribution
============

Project History and Vision
--------------------------

The journey of this project began in 2016 at a local hackathon event. The initial goal was to create a user-friendly interface for GeoDjango PointField inputs. Since then, the project has undergone numerous changes, with new widgets added for various providers and it has become a dependency for many global projects.

The current vision of the project is to develop user-friendly and developer-friendly interfaces for all GeoDjango field types using major JavaScript-based map services. If your projects require a widget that is not yet supported by django-map-widgets, you can follow this guide to contribute new widgets to the project.


Map Widget Development Overview
-------------------------------

Before beginning development, familiarize yourself with the current widget implementation approach. A typical widget consists of five main elements:

1. Django widget class implementation
2. Settings namespace Key
3. jQuery class and CSS implementation (preferably minified)
4. Widget HTML template
5. Usage documentation

As a bonus, implementing tests for your widget is highly encouraged. For optimal performance, consider using ``uglifycss`` and ``uglifyjs`` Node.js packages to generate minified versions of your static files. See `scripts.py <https://github.com/erdem/django-map-widgets/blob/main/scripts.py>`_ file to how you can automate static files minification.

if you need hand with your contribution, feel free to open a thread on `GitHub Discussions <https://github.com/erdem/django-map-widgets/discussions>`_.

Setting Up the Development Environment
--------------------------------------

The project uses a ``pyproject.toml`` file for configuration. Follow these steps to set up your development environment:

1. Install development dependencies and pre-commit hooks:

   .. code-block:: shell

       poetry install
       pre-commit install

2. Setup the demo project.


Demo Project
^^^^^^^^^^^^

The `demo project <https://github.com/erdem/django-map-widgets/tree/main/demo>`_ can serve as a development environment for creating and testing new widget types. It showcases existing widgets in both the admin interface and views.

.. image:: /_static/images/demo_project_preview.png


Setting up the Database
"""""""""""""""""""""""

To run the project, a PostgreSQL database with the PostGIS plugin is required. Follow the instructions in the `Django Installing PostGIS Documentation <https://docs.djangoproject.com/en/5.0/ref/contrib/gis/install/postgis/#post-installation>`_ to create a database with PostGIS. Update the project's ``DATABASES`` configuration in ``demo/settings.py`` if necessary.

1. Create a PostgreSQL database with PostGIS:

   .. code-block:: sql

       createdb djmap_demo
       psql djmap_demo
       CREATE EXTENSION postgis;

2. Update the ``DATABASES`` configuration in ``demo/settings.py``:

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

3. Apply database migrations:

   .. code-block:: shell

       python manage.py migrate

Environment Variables
"""""""""""""""""""""

Set the following environment variables:

.. list-table::
   :header-rows: 1

   * - Name
     - Description
   * - GOOGLE_MAP_API_KEY
     - Required for GoogleMap interactive widgets
   * - GOOGLE_MAP_API_SECRET
     - Required for GoogleMap static widgets
   * - MAPBOX_ACCESS_TOKEN
     - Required for Mapbox interactive widgets
   * - MAPBOX_ACCESS_USERNAME
     - Set if using a custom Mapbox user map style for static images

Running the Demo
""""""""""""""""

Start the development server:

.. code-block:: shell

    python manage.py runserver 0:8000

Access the demo project at `http://localhost:8000/ <http://localhost:8000/>`_.

Thanks for your contribution!

