from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.contrib.auth.models import User

admin.site.site_header = "Nepal Aircon Service"
admin.site.site_title = "Nepal Aircon Admin"
admin.site.index_title = "Management Panel"

urlpatterns = [
    path('rosunadmin/', admin.site.urls),  # ← added missing /
    path("", include("booking.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('booking/', include('booking.urls')),
    path('accounts/', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)