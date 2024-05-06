from django.urls import path, re_path
from googlemap.views import PointFieldAddView, PointFieldDetailView, PointFieldListView

app_name = "googlemap"

urlpatterns = [
    re_path(r"^pointfield/$", PointFieldListView.as_view(), name="list"),
    re_path(r"^pointfield/(?P<pk>\d+)/$", PointFieldDetailView.as_view(), name="edit"),
    re_path(r"^pointfield/add/$", PointFieldAddView.as_view(), name="add"),
]
