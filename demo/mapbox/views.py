from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView
from mapbox.forms import InteractivePointFieldViewForm
from mapbox.models import InteractivePointField


class PointFieldListView(ListView):
    queryset = InteractivePointField.objects.all()
    template_name = "mapbox/pointfield/list.html"
    context_object_name = "pointfield_objs"


class PointFieldDetailView(UpdateView):
    form_class = InteractivePointFieldViewForm
    model = InteractivePointField
    template_name = "mapbox/pointfield/edit.html"
    context_object_name = "obj"
    success_url = reverse_lazy("mapbox:list")


class PointFieldAddView(FormView):
    template_name = "mapbox/pointfield/add.html"
    form_class = InteractivePointFieldViewForm
    success_url = reverse_lazy("mapbox:list")

    def form_valid(self, form):
        form.save()
        return super(PointFieldAddView, self).form_valid(form)
