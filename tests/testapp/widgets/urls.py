from django.conf.urls import url

from .views import MapWidgetListView, PointFieldGoogleWidgetView, PointFieldGoogleStaticWidgetView, PointFieldGoogleStaticOverlayWidgetView


app_name = 'widgets'
urlpatterns = [
    url(r'^$', MapWidgetListView.as_view(), name="list"),
    url(r'^google-point-widget/$', PointFieldGoogleWidgetView.as_view(), name="google-point"),
    url(r'^google-point-static-widget/$',
        PointFieldGoogleStaticWidgetView.as_view(),
        name="google-point-static"
        ),
    url(r'^google-point-static-overlay-widget/$',
        PointFieldGoogleStaticOverlayWidgetView.as_view(),
        name="google-point-static-overlay"
        ),
]


