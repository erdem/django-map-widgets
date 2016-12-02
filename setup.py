import os
from setuptools import setup, find_packages

VERSION = (0, 1, 7)
__version__ = '.'.join(map(str, VERSION))

readme_rst = os.path.join(os.path.dirname(__file__), 'README.rst')

if os.path.exists(readme_rst):
    long_description = open(readme_rst).read()
else:
    long_description = "This module provides a few map widgets for Django applications."

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-map-widgets',
    version=__version__,
    description="Map widgets for Django PostGIS fields",
    long_description=long_description,
    author="Erdem Ozkol",
    author_email="erdemozkol@gmail.com",
    url="https://github.com/erdem/django-map-widgets",
    license="MIT",
    platforms=["any"],
    packages=find_packages(exclude=("example", "static", "env")),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python",
    ],
)

