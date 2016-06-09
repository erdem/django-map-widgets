from django.views.generic import FormView

from cities.forms import CityForm


class CityCreateView(FormView):
    template_name = "cities/form.html"
    form_class = CityForm

