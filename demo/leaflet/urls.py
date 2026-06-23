from django.urls import path, re_path
from leaflet.views import (
    PointFieldAddView,
    PointFieldDetailView,
    PointFieldListView,
    PolygonFieldAddView,
    PolygonFieldDetailView,
    PolygonFieldListView,
)

app_name = "leaflet"

urlpatterns = [
    re_path(r"^pointfield/$", PointFieldListView.as_view(), name="list"),
    re_path(r"^pointfield/(?P<pk>\d+)/$", PointFieldDetailView.as_view(), name="edit"),
    re_path(r"^pointfield/add/$", PointFieldAddView.as_view(), name="add"),
    re_path(r"^polygonfield/$", PolygonFieldListView.as_view(), name="polygon-list"),
    re_path(
        r"^polygonfield/(?P<pk>\d+)/$",
        PolygonFieldDetailView.as_view(),
        name="polygon-edit",
    ),
    re_path(r"^polygonfield/add/$", PolygonFieldAddView.as_view(), name="polygon-add"),
]
