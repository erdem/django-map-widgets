import mapwidgets

from django.contrib import admin
from django.contrib.gis.db import models

from .models import PointField


class PointFieldAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": mapwidgets.GooglePointFieldWidget}
    }
    list_display = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'location')}),
        ('Extra', {
            'fields': ('city',),
            'classes': ('collapse',),
        }),
    )


admin.site.register(PointField, PointFieldAdmin)
