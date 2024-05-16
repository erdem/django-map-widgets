from django import forms
from googlemap.models import InteractivePointField

from mapwidgets import GoogleMapPointFieldWidget


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
