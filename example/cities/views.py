from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView

from cities.forms import CityCreateForm, CityDetailForm
from cities.models import City


class CityListView(ListView):
    queryset = City.objects.all()
    template_name = "cities/list.html"
    context_object_name = "cities"


class CityDetailView(UpdateView):
    form_class = CityDetailForm
    model = City
    template_name = "cities/detail.html"


class CityCreateView(FormView):
    template_name = "cities/form.html"
    form_class = CityCreateForm
    success_url = reverse_lazy("cities:list")

    def form_valid(self, form):
        form.save()
        return super(CityCreateView, self).form_valid(form)






