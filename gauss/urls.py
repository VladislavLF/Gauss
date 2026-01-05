from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from tasks.views import pageNotFound


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('captcha/', include('captcha.urls')),
]

handler404 = pageNotFound

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
