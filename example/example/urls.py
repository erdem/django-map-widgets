from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('cities:list'))),
    url(r'^admin/', admin.site.urls),
    url(r'^cities/', include('cities.urls', namespace='cities')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
