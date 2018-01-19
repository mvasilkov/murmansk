from django.contrib import admin

from .models import Disk, File, FileCopy, Oplog


@admin.register(Disk)
class DiskAdmin(admin.ModelAdmin):
    list_display = ('name', 'coupling', 'dev_name', 'mount_point', 'is_healthy')


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('short_sha256', 'name', 'media_class', 'readable_size', 'readable_copies')
    readonly_fields = ('size', 'sha256')


@admin.register(FileCopy)
class FileCopyAdmin(admin.ModelAdmin):
    list_display = ('path', 'disk', 'is_healthy', 'last_checked')


@admin.register(Oplog)
class OplogAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'error_code')
    readonly_fields = ('error_code', 'stdout', 'stderr')
