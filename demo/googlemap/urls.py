from django.urls import path
from googlemap.views import (
    PointFieldInteractiveAddView,
    PointFieldInteractiveEditView,
    PointFieldInteractiveListView,
)

app_name = "googlemap"

urlpatterns = [
    path(
        "pointfield/interactive/",
        PointFieldInteractiveListView.as_view(),
        name="pointfield_interactive_list",
    ),
    path(
        "pointfield/interactive/<int:pk>/",
        PointFieldInteractiveEditView.as_view(),
        name="pointfield_interactive_edit",
    ),
    path(
        "pointfield/interactive/add/",
        PointFieldInteractiveAddView.as_view(),
        name="pointfield_interactive_add",
    ),
]
