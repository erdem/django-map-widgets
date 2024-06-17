
.. _contribution_doc:


============
Contribution
============

The journey of this project began in 2016 at a local hackathon event. The initial goal was to create a user-friendly interface for GeoDjango PointField inputs. Since its inception, the project has undergone numerous changes, with new widgets added for various providers and it has become a dependency for many global projects.

The current vision of the project is to develop user-friendly and developer-friendly interfaces for all GeoDjango field types using major JavaScript-based map services. If your projects require a widget that is not yet supported by django-map-widgets, you can follow this guide to contribute new widgets to the project.


Demo Project
------------

This is an example Django project that demonstrates the usage of all widgets with various settings in Django admin and views.

.. image:: https://github.com/erdem/django-map-widgets/assets/1518272/adc78ac4-4a09-4423-92a9-5b3c44b996f5
   :width: 1158
   :alt: Screenshot 2024-06-16 at 17 00 26

Setup
^^^^^

To run the project, a PostgreSQL database with the PostGIS plugin is required. Follow the instructions in the `Django Installing PostGIS Documentation <https://docs.djangoproject.com/en/5.0/ref/contrib/gis/install/postgis/#post-installation>`_ to create a database with PostGIS. Update the project's ``DATABASES`` configuration in ``demo/settings.py`` if necessary.

Create and configure the database:

.. code-block:: shell

    createdb djmap_demo
    psql djmap_demo
    CREATE EXTENSION postgis;

Apply database migrations and load sample fixtures:

.. code-block:: shell

    python manage.py migrate
    python manage.py loaddata fixtures/*.json

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




1. **Fork the Repository:**
   Start by forking the Django Map Widgets repository on GitHub to your own account.

2. **Clone the Repository:**
   Clone your forked repository to your local machine.

   ```shell
   git clone https://github.com/yourusername/django-map-widgets.git
   cd django-map-widgets
   ```

3. **Set Up the Demo Project:**
   To ensure your changes work correctly, set up the demo project. This will help you test the widgets with various settings in Django admin and views.

   **Setting up PostgreSQL with PostGIS:**

   Follow the instructions in the [Django documentation](https://docs.djangoproject.com/en/5.0/ref/contrib/gis/install/postgis/#post-installation) to create a PostgreSQL database with PostGIS. Update the `DATABASES` configuration in `demo/settings.py` if necessary.

   ```shell
   createdb djmap_demo
   psql djmap_demo
   CREATE EXTENSION postgis;
   ```

   **Apply Migrations and Load Sample Fixtures:**

   ```shell
   python manage.py migrate
   python manage.py loaddata fixtures/*.json
   ```

   **Run the Development Server:**

   ```shell
   python manage.py runserver 0:8000
   ```

4. **Make Your Changes:**
   Create a new branch for your changes and make your modifications.

   ```shell
   git checkout -b your-feature-branch
   ```

5. **Write Tests and Documentation:**
   Ensure your changes are well-tested. Add or update documentation to explain your changes and how to use new features.

6. **Commit Your Changes:**
   Commit your changes with clear and concise commit messages.

   ```shell
   git add .
   git commit -m "Description of your changes"
   ```

7. **Push to Your Fork:**
   Push your changes to your forked repository.

   ```shell
   git push origin your-feature-branch
   ```

8. **Create a Pull Request:**
   Open a pull request to the main repository. Provide a detailed description of your changes and include any relevant information or links to issues you are addressing.

   **Note:** Ensure your pull request includes sufficient documentation and setup instructions for the demo project.

Thank you for contributing to Django Map Widgets!
