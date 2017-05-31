from django.views.generic import TemplateView


class MapWidgetListView(TemplateView):
    template_name = "widgets/widget_list.html"


class PointFieldGoogleWidgetView(TemplateView):
    template_name = "widgets/google_point_widget.html"


class PointFieldGoogleStaticWidgetView(TemplateView):
    template_name = "widgets/google_point_static_widget.html"


class PointFieldGoogleStaticOverlayWidgetView(TemplateView):
    template_name = "widgets/google_point_static_overlay_widget.html"



