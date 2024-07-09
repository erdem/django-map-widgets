import os

from setuptools import find_packages, setup

VERSION = (0, 5, 1)
__version__ = ".".join(map(str, VERSION))


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
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
