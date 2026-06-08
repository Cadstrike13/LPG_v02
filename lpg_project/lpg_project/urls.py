from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('dj_admin/', admin.site.urls),
    path('', include('lpg.urls')),  # redirige vers lpg/urls.py pour les endpoints API
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
