from django import forms

from cities.models import City
from mapwidgets.widgets import GoogleMapWidget


class CityForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ("name", "coordinates", "city_hall")
        widgets = {
            'coordinates': GoogleMapWidget,
            'city_hall': GoogleMapWidget,
        }