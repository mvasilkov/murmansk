from datetime import datetime
from os.path import basename, getsize, realpath, relpath
from subprocess import CalledProcessError

from django.core.management.base import BaseCommand, CommandError

from diskarray.models import Disk, File, FileCopy, Oplog
from mur import MUR_DISK
from mur.commands import sha256


class Command(BaseCommand):
    help = 'Add existing file'

    def add_arguments(self, parser):
        parser.add_argument('disk')
        parser.add_argument('path')

    def handle(self, *args, **options):
        self.stdout.write('---')
        mur_disk = options['disk']
        if not mur_disk:
            raise CommandError('%s is required' % MUR_DISK)

        path = options['path']
        if not path:
            raise CommandError('Path is required')

        path = realpath(path)
        self.stdout.write('Path = %s' % path)
        try:
            size = getsize(path)
        except OSError:
            raise CommandError('File not found | inaccessible')

        disk = Disk.from_file(mur_disk)
        self.stdout.write('Disk = %s' % disk)
        if disk.should_be_mounted() and not disk.is_mounted():
            raise CommandError('Disk is not mounted')
        assert disk.live_mount_point

        try:
            shasum = sha256(path)
        except CalledProcessError as err:
            oplog = Oplog(
                command=err.cmd,
                stage=Oplog.ENDED,
                error_code=err.returncode,
                stdout=err.stdout,
                stderr=err.stderr)
            oplog.save()
            raise

        self.stdout.write('SHA-256 = %s' % shasum)
        try:
            existing_file = File.objects.get(sha256=shasum)
        except File.DoesNotExist:
            existing_file = None
        else:
            self.stdout.write('Existing file: %s' % existing_file)

        if existing_file is None:
            file = File(name=basename(path), size=size, sha256=shasum)
            file.media_class = file.guess_media_class()
            file.save()
            self.stdout.write('New file: %s' % file)
        else:
            file = existing_file

        copy = FileCopy(
            disk=disk,
            file=file,
            path=relpath(path, disk.live_mount_point),
            is_healthy=True,
            last_checked=datetime.now())
        copy.save()
