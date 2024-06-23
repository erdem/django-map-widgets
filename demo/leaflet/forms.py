from django import forms
from leaflet.models import InteractivePointField

from mapwidgets import LeafletPointFieldWidget


class InteractivePointFieldViewForm(forms.ModelForm):
    class Meta:
        model = InteractivePointField
        fields = ("name", "location")
        widgets = {
            "location": LeafletPointFieldWidget,
        }
