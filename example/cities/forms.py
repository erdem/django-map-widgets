from django import forms

from cities.models import City
from mapwidgets.widgets import GooglePointFieldWidget


class CityForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ("name", "coordinates", "city_hall")
        widgets = {
            'coordinates': GooglePointFieldWidget,
            'city_hall': GooglePointFieldWidget,
        }