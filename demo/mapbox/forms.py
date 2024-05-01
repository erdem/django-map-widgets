from django import forms

from mapbox.models import InteractivePointField
from mapwidgets import MapboxPointFieldWidget


class InteractivePointFieldViewForm(forms.ModelForm):

    class Meta:
        model = InteractivePointField
        fields = ("name", "location")
        widgets = {
            "location": MapboxPointFieldWidget,
        }
