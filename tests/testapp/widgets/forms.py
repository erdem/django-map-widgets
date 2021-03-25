from django import forms

from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticMapWidget, GoogleStaticOverlayMapWidget
from .models import PointField


class PointFieldCreateForm(forms.ModelForm):

    class Meta:
        model = PointField
        fields = ("name", "location", "city")
        widgets = {
            'location': GooglePointFieldWidget,
            'city': GooglePointFieldWidget,
        }
