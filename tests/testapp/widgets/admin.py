import mapwidgets

from django.contrib import admin
from django.contrib.gis.db import models

from .models import PointField, Street


class StreetInline(admin.TabularInline):
    model = Street
    formfield_overrides = {
        models.PointField: {"widget": mapwidgets.GooglePointFieldWidget}
    }
    extra = 2
    

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
    inlines = [StreetInline]


admin.site.register(PointField, PointFieldAdmin)
