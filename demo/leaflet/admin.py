from django.contrib.gis import admin
from django.contrib.gis.db import models
from leaflet import models as leaflet_models

import mapwidgets


class InteractivePointFieldAdmin(admin.ModelAdmin):
    list_display = ("name",)
    formfield_overrides = {
        models.PointField: {"widget": mapwidgets.LeafletPointFieldWidget}
    }


admin.site.register(leaflet_models.InteractivePointField, InteractivePointFieldAdmin)
