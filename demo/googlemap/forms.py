from django import forms
from googlemap.models import InteractivePointField

from mapwidgets import GoogleMapPointFieldWidget


class InteractivePointFieldViewForm(forms.ModelForm):

    class Meta:
        model = InteractivePointField
        fields = ("name", "location")
        widgets = {
            "location": GoogleMapPointFieldWidget,
        }
