"""Various development related automation scripts to run with Poetry run"""

from logging import INFO
from pathlib import Path

import click
from citizenshell import LocalShell
from django.conf import settings

from demo.demo import settings as demo__project_settings

# initialise demo project django settings to skip `ImproperlyConfigured` errors
settings.configure(demo__project_settings)

from mapwidgets.settings import mw_settings

shell = LocalShell(log_level=INFO)


@click.group()
def cli():
    pass


def install_js_dependencies():
    """
    Install uglifycss and uglifyjs CLI to minify the static files.
    """
    shell("npm install uglify-js -g")
    shell("npm install uglifycss -g")


DJMAP_PATH = Path(__file__).resolve().parent  # "django-map-widgets/"
MW_STATIC_PATH = DJMAP_PATH / "mapwidgets" / "static"


def _static_absolute_path(media_path):
    return str(MW_STATIC_PATH / Path(media_path))


def minify_js_files():
    """
    Generate UglifyJS command to run minify execution for js files
    """
    _JS_MAPPING = {
        "GoogleMapPointFieldWidget": {
            "dev_js_paths": mw_settings.GoogleMap.PointField.interactive.media.js.dev,
            "minified_js_path": mw_settings.GoogleMap.PointField.interactive.media.js.minified,
        },
        "GoogleMapPointFieldInlineWidget": {
            "dev_js_paths": mw_settings.GoogleMap.PointField.interactive.media.js.dev
            + [
                "mapwidgets/js/pointfield/interactive/googlemap/mw_pointfield_inline_generator.js"
            ],
            "minified_js_path": [
                "mapwidgets/js/pointfield/interactive/googlemap/mw_pointfield_inline.min.js"
            ],
        },
        "MapboxPointFieldWidget": {
            "dev_js_paths": mw_settings.Mapbox.PointField.interactive.media.js.dev,
            "minified_js_path": mw_settings.Mapbox.PointField.interactive.media.js.minified,
        },
        "LeafletPointFieldWidget": {
            "dev_js_paths": mw_settings.Leaflet.PointField.interactive.media.js.dev,
            "minified_js_path": mw_settings.Leaflet.PointField.interactive.media.js.minified,
        },
        "MagnificPopup": {
            "dev_js_paths": ["mapwidgets/js/staticmap/mw_jquery.magnific-popup.js"],
            "minified_js_path": [
                "mapwidgets/js/staticmap/mw_jquery.magnific-popup.min.js"
            ],
        },
    }

    for k, v in _JS_MAPPING.items():
        absolute_paths = [_static_absolute_path(m) for m in v["dev_js_paths"]]
        input_files = " ".join(absolute_paths)
        output_file = _static_absolute_path(v["minified_js_path"][0])
        uglifyjs_command = "uglifyjs {input_files} -o {output_file}".format(
            input_files=input_files, output_file=output_file
        )
        shell(uglifyjs_command)


def minify_css_files():
    """
    Generate UglifyCSS command to run minify execution for css files
    """
    _CSS_MAPPING = {
        "input_files": _static_absolute_path("mapwidgets/css/map_widgets.css"),
        "output_file": _static_absolute_path("mapwidgets/css/map_widgets.min.css"),
    }

    uglifycss_command = "uglifycss {input_files} > {output_file}".format(
        input_files=_CSS_MAPPING["input_files"], output_file=_CSS_MAPPING["output_file"]
    )
    shell(uglifycss_command)


@cli.command()
def minify_static_files():
    """
    Minify JS and CSS files of the widgets
    """
    minify_js_files()
    minify_css_files()


def run_black():
    shell("black .")


def run_isort():
    shell("isort .")


@cli.command()
def run_ci_jobs():
    run_black()
    run_isort()


def build_pypi_package():
    shell("python setup.py sdist bdist_wheel")
    shell("twine check dist/*")


def publish_test_pypi_package():
    shell("twine upload --repository-url https://test.pypi.org/legacy/ dist/*")


if __name__ == "__main__":
    cli()
