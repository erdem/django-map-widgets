from __future__ import unicode_literals

from django.contrib.gis.db import models


class PointField(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField(srid=4326)
    city = models.PointField(blank=True, null=True, srid=3857)

    def __str__(self):
        return self.name


class PointFieldInline(models.Model):
    point = models.ForeignKey(PointField)
    name = models.CharField(max_length=255, blank=True)
    coordinate = models.PointField()

    def __str__(self):
        return self.name
