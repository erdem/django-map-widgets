from django.conf.urls import url
from cities.views import CityCreateView, CityListView, CityDetailView

urlpatterns = [
    url(r'^$', CityListView.as_view(), name="list"),
    url(r'^(?P<pk>\d+)/$', CityDetailView.as_view(), name="detail"),
    url(r'^create/$', CityCreateView.as_view(), name="create"),
]