from django import forms
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


class StaticPointFieldAdmin(admin.ModelAdmin):
    list_display = ("name",)
    formfield_overrides = {
        models.PointField: {"widget": mapwidgets.GoogleMapPointFieldWidget}
    }

    def add_view(self, request, form_url="", extra_context=None):
        return super().add_view(request, form_url, extra_context)

    def get_form(self, request, obj=None, change=False, **kwargs):
        if change:  # Catch if admin renders edit item page

            class StaticPointFieldAdminForm(forms.ModelForm):
                class Meta:
                    fields = "__all__"
                    model = googlemap_models.StaticPointField
                    widgets = {
                        "location": mapwidgets.GoogleMapPointFieldStaticWidget,
                        "location_optional": mapwidgets.GoogleMapPointFieldStaticWidget,
                    }

            self.form = StaticPointFieldAdminForm
        return super().get_form(request, obj, change, **kwargs)


admin.site.register(googlemap_models.InteractivePointField, InteractivePointFieldAdmin)
admin.site.register(googlemap_models.StaticPointField, StaticPointFieldAdmin)
