from django import forms
from mapbox.models import InteractivePointField, StaticPointField

from mapwidgets import MapboxPointFieldStaticWidget, MapboxPointFieldWidget


class InteractivePointFieldViewForm(forms.ModelForm):
    class Meta:
        model = InteractivePointField
        fields = ("name", "location")
        widgets = {
            "location": MapboxPointFieldWidget,
        }


class StaticPointFieldViewForm(forms.ModelForm):
    class Meta:
        model = StaticPointField
        fields = ("name", "location", "location_has_default")
        widgets = {
            "location": MapboxPointFieldStaticWidget,
            "location_has_default": MapboxPointFieldStaticWidget(
                settings={"enableMagnificPopup": False}
            ),
        }
