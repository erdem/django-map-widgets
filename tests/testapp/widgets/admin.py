import mapwidgets

from django.contrib import admin
from django.contrib.gis.db import models

from widgets.models import PointField


class PointFieldAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": mapwidgets.GooglePointFieldWidget}
    }

admin.site.register(PointField, PointFieldAdmin)
