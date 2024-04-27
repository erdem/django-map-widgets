from django.contrib.gis import admin
from django.contrib.gis.db import models

import mapwidgets

from googlemap import models as googlemap_models


class InteractiveAdminInline(admin.TabularInline):
    model = googlemap_models.InteractiveInlinePointField
    fk_name = "point"
    extra = 1
    formfield_overrides = {
        models.PointField: {"widget": mapwidgets.GoogleMapPointFieldInlineWidget}
    }


class InteractivePointFieldAdmin(admin.ModelAdmin):
    list_display = ("name",)
    formfield_overrides = {
        models.PointField: {"widget": mapwidgets.GoogleMapPointFieldWidget}
    }
    inlines = [InteractiveAdminInline]


admin.site.register(googlemap_models.InteractivePointField, InteractivePointFieldAdmin)