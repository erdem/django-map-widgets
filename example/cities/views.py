from django.views.generic import FormView, ListView

from cities.forms import CityForm
from cities.models import City


class CityListView(ListView):
    queryset = City.objects.all()
    template_name = "cities/list.html"
    context_object_name = "cities"


class CityCreateView(FormView):
    template_name = "cities/form.html"
    form_class = CityForm


