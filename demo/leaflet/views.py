from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView
from leaflet.forms import InteractivePointFieldViewForm, InteractivePolygonFieldViewForm
from leaflet.models import InteractivePointField, InteractivePolygonField


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


class PolygonFieldListView(ListView):
    queryset = InteractivePolygonField.objects.all().order_by("-updated_at")
    template_name = "leaflet/polygonfield/list.html"
    context_object_name = "polygonfield_objs"


class PolygonFieldDetailView(UpdateView):
    form_class = InteractivePolygonFieldViewForm
    model = InteractivePolygonField
    template_name = "leaflet/polygonfield/edit.html"
    context_object_name = "obj"
    success_url = reverse_lazy("leaflet:polygon-list")


class PolygonFieldAddView(FormView):
    template_name = "leaflet/polygonfield/add.html"
    form_class = InteractivePolygonFieldViewForm
    success_url = reverse_lazy("leaflet:polygon-list")

    def form_valid(self, form):
        form.save()
        return super(PolygonFieldAddView, self).form_valid(form)
