from django import forms
from leaflet.models import InteractivePointField, InteractivePolygonField

from mapwidgets import LeafletPointFieldWidget, LeafletPolygonFieldWidget


class InteractivePointFieldViewForm(forms.ModelForm):
    class Meta:
        model = InteractivePointField
        fields = ("name", "location")
        widgets = {
            "location": LeafletPointFieldWidget,
        }


class InteractivePolygonFieldViewForm(forms.ModelForm):
    class Meta:
        model = InteractivePolygonField
        fields = ("name", "area")
        widgets = {
            "area": LeafletPolygonFieldWidget,
        }
