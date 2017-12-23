from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import Picture, Folder


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('short_sha256', 'file', 'width', 'height', 'readable_size')
    readonly_fields = ('height', 'width', 'size', 'sha256')


@admin.register(Folder)
class FolderAdmin(MPTTModelAdmin):
    list_display = ['name']
