from django.urls import path
from cities.views import CityCreateView, CityListView, CityDetailView

app_name = 'cities'

urlpatterns = [
    path(r'^$', CityListView.as_view(), name="list"),
    path(r'^(?P<pk>\d+)/$', CityDetailView.as_view(), name="detail"),
    path(r'^create/$', CityCreateView.as_view(), name="create"),
]