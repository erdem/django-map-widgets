import os
from fabric.api import local


JS_FILE_MAPPING = {
    "GooglePointFieldWidget": {
        "input_files": [
            "mapwidgets/static/mapwidgets/js/jquery_class.js",
            "mapwidgets/static/mapwidgets/js/django_mw_base.js",
            "mapwidgets/static/mapwidgets/js/mw_google_point_field.js",

        ],
        "output_file": "mapwidgets/static/mapwidgets/js/mw_google_point_field.min.js"
    },
    "GooglePointFieldInlineWidget": {
        "input_files": [
            "mapwidgets/static/mapwidgets/js/jquery_class.js",
            "mapwidgets/static/mapwidgets/js/django_mw_base.js",
            "mapwidgets/static/mapwidgets/js/mw_google_point_field.js",
            "mapwidgets/static/mapwidgets/js/mw_google_point_field_generater.js",
        ],
        "output_file": "mapwidgets/static/mapwidgets/js/mw_google_point_inline_field.min.js"
    }
}


CSS_FILE_MAPPING = {
    "GooglePointFieldWidget": {
        "input_files": [
            "mapwidgets/static/mapwidgets/css/map_widgets.css",

        ],
        "output_file": "mapwidgets/static/mapwidgets/css/map_widgets.min.css"
    },
    "GoogleStaticOverlayMapWidget": {
        "input_files": [
            "mapwidgets/static/mapwidgets/css/magnific-popup.css",
        ],
        "output_file": "mapwidgets/static/mapwidgets/css/magnific-popup.min.css",
    }
}

DJANGO_MAPWIDGETS_CONTAINER_NAME = os.environ.get('DJANGO_MAPWIDGETS_CONTAINER_NAME', 'django_mapwidgets')
POSTGRES_CONTAINER_NAME = os.environ.get('DJANGO_MAPWIDGETS_CONTAINER_NAME', 'mapwidget_postgres')


def minify_js_files():
    """
        This command minified js files with UglifyJS
    """
    for k, v in JS_FILE_MAPPING.items():
        input_files = " ".join(v["input_files"])
        output_file = v["output_file"]

        uglifyjs_command = "uglifyjs {input_files} -o {output_file}".format(
            input_files=input_files,
            output_file=output_file
        )
        local(uglifyjs_command)


def minify_css_files():
    """
        This command minified js files with UglifyCSS
    """
    for k, v in CSS_FILE_MAPPING.items():
        input_files = " ".join(v["input_files"])
        output_file = v["output_file"]

        uglifyjs_command = "uglifycss {input_files} > {output_file}".format(
            input_files=input_files,
            output_file=output_file
        )
        local(uglifyjs_command)


def minify_files():
    minify_js_files()
    minify_css_files()


def docker_build():
    local('docker-compose up --build --force-recreate')


def docker_up():
    local('docker-compose up')


def docker_shell():
    local('docker exec -it {} /bin/bash'.format(DJANGO_MAPWIDGETS_CONTAINER_NAME))


def run_on_docker(command):
    local('docker exec -it {} /bin/bash -c "{}"'.format(DJANGO_MAPWIDGETS_CONTAINER_NAME, command))


def docker_runserver():
    run_on_docker("cd tests/testapp/; python manage.py runserver 0:8000")


def docker_run_unit_tests():
    run_on_docker("cd tests/testapp/; python manage.py test")


def docker_postgres_shell():
    local('docker exec -it {} /bin/bash -c "su postgres"'.format(POSTGRES_CONTAINER_NAME))


def docker_covarage_tests():
    run_on_docker('cd tests/testapp;coverage run --source="../../mapwidgets" manage.py test;coverage report')
