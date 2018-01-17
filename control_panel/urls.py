from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from finder.views import index
from finder.oldviews import (picture, upload_picture, list_folders, select_folder, delete_folder,
                             change_folder_comment, remove_folder_comment)

urlpatterns = [
    path('', index, name='index'),
    path('files/<int:file_id>/', index, name='select_file'),
    path('folders/<int:folder_id>/', index, name='select_folder'),
    # oldviews
    path('pictures/<int:pic_id>/', picture, name='picture'),
    path('pictures/upload/', upload_picture, name='upload_picture'),
    path('folders/', list_folders, name='list_folders'),
    path('folders/<int:folder_id>/', select_folder, name='select_folder'),
    path('folders/<int:folder_id>/delete/', delete_folder, name='delete_folder'),
    path('folders/<int:folder_id>/comment/change/', change_folder_comment, name='change_folder_comment'),
    path('folders/<int:folder_id>/comment/remove/', remove_folder_comment, name='remove_folder_comment'),
    # end oldviews
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
