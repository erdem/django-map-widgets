from django import forms
from django.contrib.gis import admin
from cities.models import City, District
from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget, GooglePointFieldInlineWidget, GoogleStaticMapWidget, \
    GoogleStaticOverlayMapWidget


class DistrictAdminInline(admin.TabularInline):
    model = District
    extra = 3
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldInlineWidget}
    }


class CityAdminForm(forms.ModelForm):
    class Meta:
        model = City
        fields = "__all__"
        widgets = {
            'coordinates': GooglePointFieldWidget(settings={"GooglePointFieldWidget": (("zoom", 1),)}),
            'city_hall': GooglePointFieldWidget,
        }


class CityAdminStaticForm(forms.ModelForm):

    class Meta:
        model = City
        fields = "__all__"
        widgets = {
            'coordinates': GoogleStaticMapWidget,
            'city_hall': GoogleStaticOverlayMapWidget,
        }


class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "coordinates")
    inlines = (DistrictAdminInline,)

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = CityAdminForm
        else:
            self.form = CityAdminStaticForm
        return super(CityAdmin, self).get_form(request, obj, **kwargs)


class DistrictAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GoogleStaticOverlayMapWidget}
    }


admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)
