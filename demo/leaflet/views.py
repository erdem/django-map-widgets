from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView
from leaflet.forms import InteractivePointFieldViewForm
from leaflet.models import InteractivePointField


class PointFieldListView(ListView):
    queryset = InteractivePointField.objects.all().order_by("-updated_at")
    template_name = "leaflet/pointfield/list.html"
    context_object_name = "pointfield_objs"


class PointFieldDetailView(UpdateView):
    form_class = InteractivePointFieldViewForm
    model = InteractivePointField
    template_name = "leaflet/pointfield/edit.html"
    context_object_name = "obj"
    success_url = reverse_lazy("leaflet:list")


class PointFieldAddView(FormView):
    template_name = "leaflet/pointfield/add.html"
    form_class = InteractivePointFieldViewForm
    success_url = reverse_lazy("leaflet:list")

    def form_valid(self, form):
        form.save()
        return super(PointFieldAddView, self).form_valid(form)
