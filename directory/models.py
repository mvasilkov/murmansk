from pathlib import PurePath

from django.db import models
from django.urls import reverse
from humanfriendly import format_size
import mmh3
from mongo.objectid import ObjectId
from mur.decorators import str_method_from_attr


def _picture_path(unused, filename):
    suffix = PurePath(filename).suffix
    if suffix == '.jpg':
        suffix = '.jpeg'
    if suffix not in ('.gif', '.jpeg', '.png'):
        raise RuntimeError('Bad picture')
    path = '%s%s' % (ObjectId(), suffix)
    bucket = mmh3.hash(path, signed=False) % 16
    return '%x/%s' % (bucket, path)


@str_method_from_attr('picture')
class Picture(models.Model):
    picture = models.ImageField(upload_to=_picture_path, height_field='height', width_field='width', unique=True)
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
