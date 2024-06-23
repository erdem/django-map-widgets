from django import forms
from googlemap.models import InteractivePointField, StaticPointField

from mapwidgets import GoogleMapPointFieldStaticWidget, GoogleMapPointFieldWidget


class InteractivePointFieldViewForm(forms.ModelForm):
    class Meta:
        model = InteractivePointField
        fields = ("name", "location", "location_has_default")
        widgets = {
            "location": GoogleMapPointFieldWidget,
            "location_has_default": GoogleMapPointFieldWidget(
                settings={"mapOptions": {"scrollwheel": True}}
            ),
        }


class StaticPointFieldViewForm(forms.ModelForm):
    class Meta:
        model = StaticPointField
        fields = ("name", "location", "location_has_default")
        widgets = {
            "location": GoogleMapPointFieldStaticWidget,
            "location_has_default": GoogleMapPointFieldStaticWidget(
                settings={"enableMagnificPopup": False}
            ),
        }
