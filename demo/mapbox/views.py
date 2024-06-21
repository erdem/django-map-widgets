from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView
from mapbox.forms import InteractivePointFieldViewForm, StaticPointFieldViewForm
from mapbox.models import InteractivePointField, StaticPointField


class InteractivePointFieldListView(ListView):
    queryset = InteractivePointField.objects.all().order_by("-updated_at")
    template_name = "mapbox/pointfield/interactive/list.html"
    context_object_name = "pointfield_objs"


class InteractivePointFieldEditView(UpdateView):
    form_class = InteractivePointFieldViewForm
    model = InteractivePointField
    template_name = "mapbox/pointfield/interactive/edit.html"
    context_object_name = "obj"
    success_url = reverse_lazy("mapbox:pointfield_interactive_list")


class InteractivePointFieldAddView(FormView):
    template_name = "mapbox/pointfield/interactive/add.html"
    form_class = InteractivePointFieldViewForm
    success_url = reverse_lazy("mapbox:list")

    def form_valid(self, form):
        form.save()
        return super(InteractivePointFieldAddView, self).form_valid(form)


class StaticPointFieldListView(ListView):
    queryset = StaticPointField.objects.all().order_by("-updated_at")
    template_name = "mapbox/pointfield/static/list.html"
    context_object_name = "pointfield_objs"


class StaticPointFieldEditView(UpdateView):
    form_class = StaticPointFieldViewForm
    model = StaticPointField
    template_name = "mapbox/pointfield/static/edit.html"
    context_object_name = "obj"
    success_url = reverse_lazy("mapbox:pointfield_static_list")
