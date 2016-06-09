from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^admin/', admin.site.urls),
    url(r'^cities/', include('cities.urls', namespace='cities')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
