from django.views.generic import TemplateView, FormView

from .forms import PointFieldCreateForm


class MapWidgetListView(TemplateView):
    template_name = "widgets/widget_list.html"


class PointFieldGoogleWidgetView(FormView):
    template_name = "widgets/google_point_widget.html"
    form_class = PointFieldCreateForm
    success_url = "/"


class PointFieldGoogleStaticWidgetView(TemplateView):
    template_name = "widgets/google_point_static_widget.html"


class PointFieldGoogleStaticOverlayWidgetView(TemplateView):
    template_name = "widgets/google_point_static_overlay_widget.html"



