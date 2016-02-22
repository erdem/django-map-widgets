from setuptools import setup, find_packages

VERSION = (1, 0, 0)
__version__ = '.'.join(map(str, VERSION))


setup(
    name='django-map-widgets',
    version=__version__,
    description="Map widgets for Django",
    long_description="This module provides a few map widgets for Django applications.",
    author="Erdem Ozkol",
    author_email="erdemozkol@gmail.com",
    url="https://github.com/erdem/django-map-widgets",
    license="MIT",
    zip_safe=False,
    platforms=["any"],
    packages=find_packages(),
    package_data={
        'mapwidgets': [
            u'static/mapwidgets/*',
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python",
    ]
)

