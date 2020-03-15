from django import forms
from django.contrib.gis import admin
from .models import House, Neighbour
from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget, GooglePointFieldInlineWidget, GoogleStaticMapWidget, \
    GoogleStaticOverlayMapWidget


class NeighbourAdminInline(admin.TabularInline):
    model = Neighbour
    extra = 3
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldInlineWidget}
    }


class HouseAdminForm(forms.ModelForm):
    class Meta:
        model = House
        fields = "__all__"
        widgets = {
            'location': GooglePointFieldWidget(settings={"GooglePointFieldWidget": (("zoom", 1),)}),
            'location_has_default': GooglePointFieldWidget,
        }


class HouseAdminStaticForm(forms.ModelForm):

    class Meta:
        model = House
        fields = "__all__"
        widgets = {
            'location': GoogleStaticMapWidget,
            'location_has_default': GoogleStaticOverlayMapWidget,
        }


class HouseAdmin(admin.ModelAdmin):
    list_display = ("name", "location")
    inlines = (NeighbourAdminInline,)

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = HouseAdminForm
        else:
            self.form = HouseAdminStaticForm
        return super(HouseAdmin, self).get_form(request, obj, **kwargs)


class NeighbourAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GoogleStaticOverlayMapWidget}
    }


admin.site.register(House, HouseAdmin)
admin.site.register(Neighbour, NeighbourAdmin)

