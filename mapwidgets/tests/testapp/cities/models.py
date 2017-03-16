from __future__ import unicode_literals

from django.contrib.gis.db import models


class City(models.Model):
    name = models.CharField(max_length=255)
    coordinates = models.PointField()
    city_hall = models.PointField(blank=True, null=True)

    def __unicode__(self):
        return self.name
