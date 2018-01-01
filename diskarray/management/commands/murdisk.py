from os.path import isdir, isfile, join as joinpath, realpath

from django.core.management.base import BaseCommand, CommandError

from diskarray.models import Disk
from mur import MUR_DISK


class Command(BaseCommand):
    help = 'Create %s' % MUR_DISK

    def add_arguments(self, parser):
        parser.add_argument('disk_id', type=int)
        parser.add_argument('path')

    def handle(self, *args, **options):
        self.stdout.write('---')
        path = options['path']
        if not path:
            raise CommandError('Path is required')

        disk = Disk.objects.get(id=options['disk_id'])
        self.stdout.write('Disk = %s' % disk)

        path = realpath(path)
        self.stdout.write('Path = %s' % path)
        assert isdir(path)
        mur_disk_path = joinpath(path, MUR_DISK)
        assert not isfile(mur_disk_path)

        with open(mur_disk_path, 'w', encoding='utf-8', newline='\n') as file:
            print(disk.objectid, file=file)

        self.stdout.write('Saved %s' % mur_disk_path)

        if not disk.mount_point:
            self.stdout.write('Updating disk.mount_point')
            disk.mount_point = path
            disk.save()
