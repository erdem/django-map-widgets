from __future__ import unicode_literals

from django.contrib.gis.db import models


class PointField(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField(srid=4326)
    city = models.PointField(blank=True, null=True, srid=3857)

    def __unicode__(self):
        return self.name


class Street(models.Model):
    point = models.ForeignKey(
        PointField, blank=True, null=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=255)
    street = models.PointField(srid=4326)
