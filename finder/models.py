import hashlib
from pathlib import PurePath

from django.db import models
from django.urls import reverse
from humanfriendly import format_size
from mongo.objectid import ObjectId
from mptt.models import MPTTModel, TreeForeignKey
from mur.decorators import str_method_from_attr

BUCKET_SIZE = 1  # 4 bits


def _picture_path(unused, filename):
    suffix = PurePath(filename).suffix.lower()
    if suffix == '.jpg':
        suffix = '.jpeg'
    if suffix not in ('.gif', '.jpeg', '.png'):
        raise RuntimeError('Bad picture')
    path = '%s%s' % (ObjectId(), suffix)
    bucket = hashlib.sha256(path.encode('us-ascii')).hexdigest()[:BUCKET_SIZE]
    return '%s/%s' % (bucket, path)


@str_method_from_attr('file')
class Picture(models.Model):
    file = models.ImageField(upload_to=_picture_path, height_field='height', width_field='width', unique=True)
    height = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()
    size = models.BigIntegerField()
    sha256 = models.CharField(max_length=64, unique=True)

    def readable_size(self):
        return '%s (%s)' % (format_size(self.size, binary=True),
                            format_size(self.size))

    def short_sha256(self):
        return self.sha256[:7]

    def get_absolute_url(self):
        return reverse('picture', args=[self.id])


@str_method_from_attr('name')
class Folder(MPTTModel):
    name = models.CharField(max_length=250, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subdirectories',
                            db_index=True)
    pictures = models.ManyToManyField(Picture, related_name='folders', blank=True)
    comment = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('select_folder', args=[self.id])

    class MPTTMeta:
        order_insertion_by = ['name']
