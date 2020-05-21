from django import forms

from cities.models import City
from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticMapWidget, GoogleStaticOverlayMapWidget


class CityCreateForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ('name', 'location')
        widgets = {
            'location': GooglePointFieldWidget,
        }


class CityDetailForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ('name', 'location')
        widgets = {
            'location': GoogleStaticOverlayMapWidget(zoom=12, thumbnail_size='50x50', size='640x640'),
        }
