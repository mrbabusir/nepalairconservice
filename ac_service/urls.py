from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.contrib.auth.models import User

# ← functions must be defined BEFORE urlpatterns
def create_super(request):
    if not User.objects.filter(username='mrbabusir').exists():
        User.objects.create_superuser(
            username='mrbabusir',
            password='NepAlAiRc0n@2025!',  # ← strong password
            email='mrbabusir86@gmail.com'
        )
        return HttpResponse("Superuser created!")
    return HttpResponse("Already exists!")

admin.site.site_header = "Nepal Aircon Service"
admin.site.site_title = "Nepal Aircon Admin"
admin.site.index_title = "Management Panel"

urlpatterns = [
    path('rosunadmin/', admin.site.urls),  # ← added missing /
    path("", include("booking.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('booking/', include('booking.urls')),
    path('accounts/', include('shop.urls')),
    path('create-super/', create_super),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)