from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from directory.views import picture, upload_picture

urlpatterns = [
    path('pictures/<int:pic_id>/', picture, name='picture'),
    path('pictures/upload/', upload_picture, name='upload_picture'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
