from django.contrib.gis import admin
from django.contrib.gis.db import models
from mapbox import models as mapbox_models

import mapwidgets


@admin.register(mapbox_models.InteractivePointField)
class InteractivePointFieldAdmin(admin.ModelAdmin):
    list_display = ("name",)
    formfield_overrides = {
        models.PointField: {"widget": mapwidgets.MapboxPointFieldWidget}
    }


@admin.register(mapbox_models.StaticPointField)
class StaticPointFieldAdmin(admin.ModelAdmin):
    list_display = ("name",)
    formfield_overrides = {
        models.PointField: {"widget": mapwidgets.MapboxPointFieldStaticWidget}
    }
