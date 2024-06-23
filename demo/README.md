## Django Map Widgets Demo

This is an example Django project that demonstrates the usage of all widgets with various settings in Django admin and
views.

<img width="1158" alt="Screenshot 2024-06-16 at 17 00 26" src="https://github.com/erdem/django-map-widgets/assets/1518272/adc78ac4-4a09-4423-92a9-5b3c44b996f5">

### Setup

To run the project, a PostgreSQL database with the PostGIS plugin is required. Follow the instructions in
the [Django Installing PostGIS Documentation](https://docs.djangoproject.com/en/5.0/ref/contrib/gis/install/postgis/#post-installation)
to create a database with PostGIS. Update the project's `DATABASES` configuration in `demo/settings.py` if necessary.

Create and configure the database:

```shell
$ createdb  djmap_demo
$ psql djmap_demo
> CREATE EXTENSION postgis;
```

Apply database migrations:

```shell
python manage.py migrate
```

Set environment variables.

| Name                   | Description                                                                                             |
|------------------------|---------------------------------------------------------------------------------------------------------|
| GOOGLE_MAP_API_KEY     | Required for GoogleMap interactive widgets.                                                             |
| GOOGLE_MAP_API_SECRET  | Required for GoogleMap static widgets.                                                                  |
| MAPBOX_ACCESS_TOKEN    | Required for Mapbox interactive widgets.                                                                |
| MAPBOX_ACCESS_USERNAME | Set this if Mapbox static map images will use a custom user map style; otherwise, it can be left as is. |

Run the development server and start exploring the project at [http://localhost:8000/](http://localhost:8000/).

```shell
python manage.py runserver 0:8000
```


