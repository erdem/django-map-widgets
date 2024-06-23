from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView
from googlemap.forms import InteractivePointFieldViewForm, StaticPointFieldViewForm
from googlemap.models import InteractivePointField, StaticPointField


class InteractivePointFieldListView(ListView):
    queryset = InteractivePointField.objects.all().order_by("-updated_at")
    template_name = "googlemap/pointfield/interactive/list.html"
    context_object_name = "pointfield_objs"


class InteractivePointFieldEditView(UpdateView):
    form_class = InteractivePointFieldViewForm
    model = InteractivePointField
    template_name = "googlemap/pointfield/interactive/edit.html"
    context_object_name = "obj"
    success_url = reverse_lazy("googlemap:pointfield_interactive_list")


class InteractivePointFieldAddView(FormView):
    template_name = "googlemap/pointfield/interactive/add.html"
    form_class = InteractivePointFieldViewForm
    success_url = reverse_lazy("googlemap:pointfield_interactive_list")

    def form_valid(self, form):
        form.save()
        return super(InteractivePointFieldAddView, self).form_valid(form)


class StaticPointFieldListView(ListView):
    queryset = StaticPointField.objects.all().order_by("-updated_at")
    template_name = "googlemap/pointfield/static/list.html"
    context_object_name = "pointfield_objs"


class StaticPointFieldEditView(UpdateView):
    form_class = StaticPointFieldViewForm
    model = StaticPointField
    template_name = "googlemap/pointfield/static/edit.html"
    context_object_name = "obj"
    success_url = reverse_lazy("googlemap:pointfield_static_list")
