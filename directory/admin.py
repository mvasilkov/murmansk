from django.contrib import admin

from .models import Picture


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('short_sha256', 'picture', 'width', 'height', 'readable_size')
    readonly_fields = ('height', 'width', 'size', 'sha256')
