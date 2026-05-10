from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings

# 1. Ścieżki systemowe (zmiana języka) - BEZ przedrostka pl/en
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# 2. Ścieżki aplikacji - Z przedrostkiem pl/en (np. /pl/admin/ lub /en/login/)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('HotelApp.urls'))
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)