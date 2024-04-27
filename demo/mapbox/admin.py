from django.contrib.gis import admin
from django.contrib.gis.db import models
from mapbox import models as mapbox_models

import mapwidgets


class InteractivePointFieldAdmin(admin.ModelAdmin):
    list_display = ("name",)
    formfield_overrides = {
        models.PointField: {"widget": mapwidgets.MapboxPointFieldWidget}
    }


admin.site.register(mapbox_models.InteractivePointField, InteractivePointFieldAdmin)
