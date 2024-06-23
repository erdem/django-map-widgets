from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.urls import reverse

from demo.db import BaseModel

DEFAULT_LOCATION_POINT = Point(-104.9903, 39.7392)


class InteractivePointField(BaseModel):
    name = models.CharField(max_length=255)
    location = models.PointField(help_text="Use map widget to point the location")
    location_has_default = models.PointField(default=DEFAULT_LOCATION_POINT)
    location_optional = models.PointField(blank=True, null=True)

    class Meta:
        verbose_name = "Interactive PointField Widget"
        verbose_name_plural = "Interactive PointField Widget"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("googlemap:pointfield_interactive_edit", args=(self.id,))


class InteractiveInlinePointField(BaseModel):
    point = models.ForeignKey(InteractivePointField, on_delete=models.CASCADE)

    first_point = models.PointField(help_text="Use map widget to point the location")
    second_point = models.PointField(default=DEFAULT_LOCATION_POINT)


class StaticPointField(InteractivePointField):
    class Meta:
        proxy = True
        verbose_name = "Static PointField Widget"
        verbose_name_plural = "Static PointField Widget"

    def get_absolute_url(self):
        return reverse("googlemap:pointfield_static_edit", args=(self.id,))
