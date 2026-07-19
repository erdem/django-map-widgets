import os
import re

from setuptools import find_packages, setup

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_version():
    # Parsed as text, not imported: mapwidgets/__init__.py pulls in Django-dependent
    # widget imports that aren't safely importable during a package build.
    init_path = os.path.join(BASE_DIR, "mapwidgets", "__init__.py")
    with open(init_path, encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"^VERSION = \(([^)]+)\)", content, re.MULTILINE)
    return ".".join(part.strip() for part in match.group(1).split(","))


__version__ = get_version()

with open(os.path.join(BASE_DIR, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="django-map-widgets",
    version=__version__,
    description="Configurable and user-friendly map widgets for GeoDjango fields",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Erdem Ozkol",
    author_email="mapwidgets@erdemozkol.com",
    url="https://github.com/erdem/django-map-widgets",
    license="MIT",
    python_requires=">=3.10",
    packages=find_packages(exclude=("demo", "tests", "docs")),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="django map-widgets geodjango geolocation mapbox google map leaflet interactive-maps",
    project_urls={
        "Documentation": "https://django-map-widgets.readthedocs.io/",
        "Source": "https://github.com/erdem/django-map-widgets",
        "Demo Project": "https://github.com/erdem/django-map-widgets/tree/main/demo",
    },
)
