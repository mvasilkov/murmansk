from datetime import datetime
from os.path import join as joinpath
from subprocess import CalledProcessError

from django.core.management.base import BaseCommand, CommandError

from diskarray.models import Disk, FileCopy, Oplog
from mur import MUR_DISK
from mur.commands import sha256

from .status import CONFIDENCE_INTERVAL


class Command(BaseCommand):
    help = 'Check disk'

    def add_arguments(self, parser):
        parser.add_argument('disk')
        parser.add_argument('--everything', action='store_true')

    def handle(self, *args, **options):
        self.stdout.write('---')
        mur_disk = options['disk']
        if not mur_disk:
            raise CommandError('%s is required' % MUR_DISK)

        disk = Disk.from_file(mur_disk)
        self.stdout.write('Disk = %s' % disk)
        if disk.should_be_mounted() and not disk.is_mounted():
            raise CommandError('Disk is not mounted')
        assert disk.live_mount_point

        if options['everything']:
            copies = disk.copies.all()
        else:
            before = datetime.now() - CONFIDENCE_INTERVAL
            copies = FileCopy.objects.filter(disk=disk, last_checked__lt=before)

        for copy in copies:
            self.check_copy(disk, copy)

    def check_copy(self, disk, copy):
        self.stdout.write(f'\t- {copy.path}')
        path = joinpath(disk.live_mount_point, copy.path)

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

        if shasum == copy.file.sha256:
            copy.last_checked = datetime.now()
            copy.save()
            return

        raise NotImplementedError()
