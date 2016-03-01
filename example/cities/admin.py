from django import forms
from django.contrib.gis import admin
from cities.models import City, District
from django.contrib.gis.db import models
from mapwidgets.widgets import GoogleMapWidget


class DistrictAdminInline(admin.TabularInline):
    model = District
    extra = 3


class CityAdminForm(forms.ModelForm):
    class Meta:
        model = City
        fields = "__all__"
        widgets = {
            'coordinates': GoogleMapWidget,
        }

class CityAdmin(admin.ModelAdmin):
    inlines = (DistrictAdminInline,)
    form = CityAdminForm


class DistrictAdmin(admin.ModelAdmin):
    pass


admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)
