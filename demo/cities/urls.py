from django.urls import path, re_path
from cities.views import CityCreateView, CityListView, CityDetailView

app_name = 'cities'

urlpatterns = [
    path('', CityListView.as_view(), name="list"),
    re_path(r'^(?P<pk>\d+)/$', CityDetailView.as_view(), name="detail"),
    re_path(r'^create/$', CityCreateView.as_view(), name="create"),
]