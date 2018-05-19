from datetime import datetime
from os.path import getsize, split as splitpath
import platform
import re

from django.core.cache import cache
from django.db import models
from humanfriendly import format_size

from mongo.objectid import ObjectId
from mur import MUR_DISK
from mur.commands import mount_lines
from mur.decorators import str_method_from_attr


def _objectid():
    return str(ObjectId())


@str_method_from_attr('name')
class Disk(models.Model):
    LOCAL = 'local'
    ROAMING = 'roaming'
    COUPLING = (LOCAL, LOCAL), (ROAMING, ROAMING)

    name = models.CharField(max_length=250, unique=True)
    objectid = models.CharField(max_length=24, default=_objectid, editable=False, unique=True)
    coupling = models.CharField(max_length=10, choices=COUPLING, default=LOCAL)
    dev_name = models.CharField(max_length=20, blank=True)  # '/dev/sdb1'
    mount_point = models.CharField(max_length=40, blank=True)  # '/media/rei/A'
    is_healthy = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    pictures = models.ManyToManyField('finder.Picture', related_name='disks', blank=True)
    comment = models.TextField(blank=True)

    def is_mounted(self):
        if platform.system() == 'Windows':
            return False

        lines = cache.get_or_set('mount_lines', mount_lines)
        for line in lines:
            if line.startswith('%s on %s type' % (self.dev_name, self.mount_point)):
                return True

        return False

    def should_be_mounted(self):
        return self.coupling == Disk.LOCAL and self.dev_name and self.mount_point and platform.system() != 'Windows'

    @staticmethod
    def containing_path(path):
        for disk in Disk.objects.all():
            if disk.mount_point and path.startswith(disk.mount_point):
                return disk

        return None

    @staticmethod
    def from_file(mur_disk):
        mount_point, filename = splitpath(mur_disk)
        if filename != MUR_DISK:
            raise RuntimeError('Expected filename: %s, got: %s' % (MUR_DISK, filename))

        try:
            size = getsize(mur_disk)
        except OSError:
            raise RuntimeError('File not found | inaccessible')

        assert size == 25  # objectid + '\n'

        with open(mur_disk, 'r', encoding='us-ascii', newline='\n') as file:
            objectid = file.read()
            assert objectid.endswith('\n')
            objectid = objectid.rstrip('\n')
            assert re.fullmatch('[a-f0-9]{24}', objectid)

        disk = Disk.objects.get(objectid=objectid)
        disk.live_mount_point = mount_point
        return disk


@str_method_from_attr('name')
class File(models.Model):
    BINARY = 'binary'
    VIDEO = 'video'
    MEDIA_CLASSES = (BINARY, BINARY), (VIDEO, VIDEO)

    name = models.CharField(max_length=250)
    size = models.BigIntegerField()
    sha256 = models.CharField(max_length=64, unique=True)
    storage_class = models.PositiveSmallIntegerField(default=1)
    media_class = models.CharField(max_length=10, choices=MEDIA_CLASSES, default=BINARY)
    created = models.DateTimeField(auto_now_add=True)
    folders = models.ManyToManyField('finder.Folder', related_name='files', blank=True)
    pictures = models.ManyToManyField('finder.Picture', related_name='files', blank=True)
    comment = models.TextField(blank=True)

    def readable_copies(self):
        return 'have=%d want=%d' % (self.copies.count(), self.storage_class)

    def readable_size(self):
        return '%s (%s)' % (format_size(self.size, binary=True),
                            format_size(self.size))

    def readable_disks(self):
        return ', '.join(self.copies.values_list('disk__name', flat=True))

    def short_sha256(self):
        return self.sha256[:7]

    def guess_media_class(self):
        if self.name.endswith('.mp4') or self.name.endswith('.mkv') or self.name.endswith('.avi'):
            return File.VIDEO

        return File.BINARY


class FileCopy(models.Model):
    NEVER = datetime(1970, 1, 1)

    disk = models.ForeignKey(Disk, on_delete=models.PROTECT, related_name='copies')
    file = models.ForeignKey(File, on_delete=models.PROTECT, related_name='copies')
    path = models.CharField(max_length=1000)  # relative to disk.mount_point
    is_healthy = models.BooleanField()
    last_checked = models.DateTimeField(default=NEVER)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('disk', 'file')
        verbose_name_plural = 'file copies'

    def __str__(self):
        return '(%s) %s' % (self.disk, self.path)


class Oplog(models.Model):
    WAITING = 'waiting'
    WORKING = 'working'
    ENDED = 'ended'
    STAGES = (WAITING, WAITING), (WORKING, WORKING), (ENDED, ENDED)

    command = models.CharField(max_length=1000)
    stage = models.CharField(max_length=10, choices=STAGES, default=WAITING)
    error_code = models.SmallIntegerField(default=-1)
    stdout = models.TextField()
    stderr = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '(%s) %s' % (self.stage, self.command)
