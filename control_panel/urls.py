from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import register_converter, path

from finder.converters import ModelNameConverter
from finder.views import index, change_comment, remove_comment, rename_file, rename_folder
from finder.oldviews import (picture, upload_picture, list_folders, select_folder, delete_folder,
                             change_folder_comment, remove_folder_comment)

register_converter(ModelNameConverter, 'any')

urlpatterns = [
    path('', index, name='index'),
    path('select/<any:model_name>/<int:model_id>/', index, name='select_any'),
    path('change_comment/<any:model_name>/<int:model_id>/', change_comment, name='change_comment'),
    path('remove_comment/<any:model_name>/<int:model_id>/', remove_comment, name='remove_comment'),
    path('rename_file/<int:file_id>/', rename_file, name='rename_file'),
    path('rename_folder/<int:folder_id>/', rename_folder, name='rename_folder'),
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
