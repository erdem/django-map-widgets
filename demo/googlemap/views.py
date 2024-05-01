from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView

from googlemap.forms import InteractivePointFieldViewForm
from googlemap.models import InteractivePointField


class PointFieldListView(ListView):
    queryset = InteractivePointField.objects.all()
    template_name = "googlemap/pointfield/list.html"
    context_object_name = "pointfield_objs"


class PointFieldDetailView(UpdateView):
    form_class = InteractivePointFieldViewForm
    model = InteractivePointField
    template_name = "googlemap/pointfield/edit.html"
    context_object_name = "obj"
    success_url = reverse_lazy("googlemap:list")


class PointFieldAddView(FormView):
    template_name = "googlemap/pointfield/add.html"
    form_class = InteractivePointFieldViewForm
    success_url = reverse_lazy("googlemap:list")

    def form_valid(self, form):
        form.save()
        return super(PointFieldAddView, self).form_valid(form)
