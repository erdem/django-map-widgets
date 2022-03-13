from django import forms
from django.contrib.gis import admin
from .models import House, Neighbour
from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget, GooglePointFieldInlineWidget, GoogleStaticMapWidget, \
    GoogleStaticOverlayMapWidget, MapboxPointFieldWidget


class NeighbourAdminInline(admin.TabularInline):
    model = Neighbour
    extra = 3
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldInlineWidget}
    }


class HouseAdminStaticForm(forms.ModelForm):

    class Meta:
        model = House
        fields = "__all__"
        widgets = {
            'location': GoogleStaticOverlayMapWidget,
            'location_has_default': GoogleStaticMapWidget,
        }


class HouseAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ("name", "location")
    inlines = (NeighbourAdminInline,)
    form = HouseAdminStaticForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(HouseAdmin, self).get_form(request, obj, **kwargs)
        if obj is None:  # manipulate page form
            form.base_fields['location'].widget = MapboxPointFieldWidget()
            form.base_fields['location_has_default'].widget = GooglePointFieldWidget()
        return form

    @property
    def media(self):
        media = super().media
        return media

    def _changeform_view(self, request, object_id, form_url, extra_context):
        return super()._changeform_view(request, object_id, form_url, extra_context)


class NeighbourAdmin(admin.ModelAdmin):
    autocomplete_fields = ('neighbour_of_house',)
    formfield_overrides = {
        models.PointField: {"widget": MapboxPointFieldWidget}
    }


admin.site.register(House, HouseAdmin)
admin.site.register(Neighbour, NeighbourAdmin)

