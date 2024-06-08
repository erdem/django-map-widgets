from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView
from googlemap.forms import InteractivePointFieldViewForm
from googlemap.models import InteractivePointField


class PointFieldInteractiveListView(ListView):
    queryset = InteractivePointField.objects.all()
    template_name = "googlemap/pointfield/interactive/list.html"
    context_object_name = "pointfield_objs"


class PointFieldInteractiveEditView(UpdateView):
    form_class = InteractivePointFieldViewForm
    model = InteractivePointField
    template_name = "googlemap/pointfield/interactive/edit.html"
    context_object_name = "obj"
    success_url = reverse_lazy("googlemap:pointfield_interactive_list")


class PointFieldInteractiveAddView(FormView):
    template_name = "googlemap/pointfield/interactive/add.html"
    form_class = InteractivePointFieldViewForm
    success_url = reverse_lazy("googlemap:pointfield_interactive_list")

    def form_valid(self, form):
        form.save()
        return super(PointFieldInteractiveAddView, self).form_valid(form)
