from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

DEFAULT_LOCATION_POINT = Point(-104.9903, 39.7392)


class House(models.Model):
    location = models.PointField(help_text="Use map widget for point the house location")
    name = models.CharField(max_length=255)
    location_has_default = models.PointField(default=DEFAULT_LOCATION_POINT)

    def __str__(self):
        return self.name


class Neighbour(models.Model):
    neighbour_of_house = models.ForeignKey(House, on_delete=models.CASCADE)

    location = models.PointField(null=True, blank=True)
    address = models.TextField()

    def __str__(self):
        return self.address


class City(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField(help_text="Use map widget for point the house location")

    def __str__(self):
        return self.name
