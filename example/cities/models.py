from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

POINT = Point(-104.9903, 39.7392, srid=4326)


class City(models.Model):
    name = models.CharField(max_length=255)
    coordinates = models.PointField(help_text="To generate the map for your location")
    city_hall = models.PointField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class District(models.Model):
    city = models.ForeignKey(City)
    name = models.CharField(max_length=255)
    location = models.PointField(help_text="To generate the map for your location")

    def __unicode__(self):
        return self.name