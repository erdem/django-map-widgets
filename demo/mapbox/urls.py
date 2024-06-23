from django.urls import path
from mapbox.views import (
    InteractivePointFieldAddView,
    InteractivePointFieldEditView,
    InteractivePointFieldListView,
    StaticPointFieldEditView,
    StaticPointFieldListView,
)

app_name = "mapbox"

urlpatterns = [
    path(
        "pointfield/interactive/",
        InteractivePointFieldListView.as_view(),
        name="pointfield_interactive_list",
    ),
    path(
        "pointfield/interactive/<int:pk>/",
        InteractivePointFieldEditView.as_view(),
        name="pointfield_interactive_edit",
    ),
    path(
        "pointfield/interactive/add/",
        InteractivePointFieldAddView.as_view(),
        name="pointfield_interactive_add",
    ),
    path(
        "pointfield/static/",
        StaticPointFieldListView.as_view(),
        name="pointfield_static_list",
    ),
    path(
        "pointfield/static/<int:pk>/",
        StaticPointFieldEditView.as_view(),
        name="pointfield_static_edit",
    ),
]
