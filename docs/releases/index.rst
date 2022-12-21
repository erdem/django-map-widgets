=============
Release Notes
=============


0.4.1
^^^^^

   -  Added scroll wheel zooming functionality switch to Google Point Map Settings. (#134)
   -  Added Chinese(ZH) localisation support. (#133)


0.4.0
^^^^^

   -  Supported MapBox Map for Geo Point Field
   -  Fixed javascript triggers undefined place object binding issue. (#125)
   -  Documented MapBox point field map widget
   -  Updated various localize files.

0.3.3
^^^^^

   -  Replaced
      `ugettext_lazy <https://github.com/erdem/django-map-widgets/pull/127>`__
      usages with
      `gettext_lazy <https://docs.djangoproject.com/en/4.0/releases/4.0/#features-removed-in-4-0>`__
      for Django 4.0. (#127)
   -  Updated `Travis CI
      file <https://github.com/erdem/django-map-widgets/pull/129>`__.
      (#129)

0.3.1
^^^^^

   -  Added
      `streetViewControl <https://developers.google.com/maps/documentation/javascript/streetview#StreetViewMapUsage>`__
      switch to GooglePointFieldWidget settings. (#124)

0.3.1
^^^^^

   -  Removed ``six`` package usages. (#117)
   -  Added a new general widget setting in order to specify Google JS
      libraries. (#119)
   -  Implemented some improvements for the demo project.

0.3.0
^^^^^
   -  Implemented a new demo project with Django 2.x.
   -  Fixed Django Admin jQuery conflicts. (#100)
   -  Fixed a new widget JS instance initialising issue for Django Admin
      Inlines. (#84)
   -  Added Python 3.8 env settings to TravisCI configuration.

0.2.3
^^^^^

   -  Fixed python ``six`` module import issue.
   -  Fixed PostGIS setup errors in CI pipeline.
   -  Added Estonian language support.


0.2.0
^^^^^

    -  Fixed Python 3.6, Django 2.x compatible issues.
    -  Fixed SRID format converter issues.
    -  Removed ``pyproj`` package dependency.
    -  Various development infrastructure updates. (Docker, Fabric files
      etc.)
    -  Point map widget JS objects associated to the map HTML elements
      with jQuey ``$.data`` method.
    -  Passing Google Place AutoComplete full response object to jQuery
      triggers.

0.1.9
^^^^^

    - Google Place Autocomplete object binding to jQuery triggers.
    - Implemented Google Geocoding support for the marker coordinates.
    - Added custom widget settings feature for each widget.
    - Added Portuguese localisation support.
    - Fixed Google Place Autocomplete widget bugs in Django Admin Inlines.
    - Fixed Python 3.6 errors.
    - Fixed Javascript bugs.
    - The GitHub repository Integrated with Travis CI.
    - Implemented unit tests for backend code. (%100 code coverage)
    - Change development environment from Vagrant to Docker.

0.1.8
^^^^^

    - Full documentation integrated to readthedocs.org.
    - Fixed Google Map static widget issues.
    - Added Russian localisation support.
    - Added `Google Places Autocomplete <https://developers.google.com/maps/documentation/javascript/places-autocomplete>`_ options support.
    - Fixed CSS issues.
