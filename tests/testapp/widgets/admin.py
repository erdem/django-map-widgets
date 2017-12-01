import mapwidgets

from django.contrib import admin
from django.contrib.gis.db import models

from .models import PointField, PointFieldInline


class PointFieldAdminInline(admin.StackedInline):
    model = PointFieldInline
    extra = 3
    formfield_overrides = {
        models.PointField: {"widget": mapwidgets.GooglePointFieldInlineWidget}
    }


class PointFieldAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": mapwidgets.GooglePointFieldWidget}
    }
    list_display = ('name', 'location_text', 'city_text')
    readonly_fields = ('location_text', 'city_text')
    fieldsets = (
        (None, {'fields': ('name', 'location')}),
        ('Extra', {
            'fields': ('city',),
            'classes': ('collapse',),
        }),
    )
    inlines = [
        PointFieldAdminInline
    ]

    def location_text(self, obj):
        return obj.location.get_coords()

    def city_text(self, obj):
        if obj.city:
            return obj.city.get_coords()
        return ""


admin.site.register(PointField, PointFieldAdmin)
