from django.conf.urls import url
from cities.views import CityCreateView

urlpatterns = [
    # url(r'^$', CityListView.as_view(), name="list"),
    url(r'^(?P<pk>[0-9]+)/$', CityCreateView.as_view(), name="create"),
]