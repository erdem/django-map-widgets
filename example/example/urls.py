from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cities/', include('cities.urls', namespace='cities')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)