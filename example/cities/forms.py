from django import forms

from cities.models import City
from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticMapWidget, GoogleStaticOverlayMapWidget


class CityCreateForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ("name", "coordinates", "city_hall")
        widgets = {
            'coordinates': GooglePointFieldWidget,
            'city_hall': GooglePointFieldWidget,
        }


class CityDetailForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ("name", "coordinates", "city_hall")
        widgets = {
            'coordinates': GoogleStaticMapWidget,
            'city_hall': GoogleStaticOverlayMapWidget,
        }
