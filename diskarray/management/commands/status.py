from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db.models import Count, Q

from diskarray.models import Disk, FileCopy

CONFIDENCE_INTERVAL = timedelta(days=60)


class Command(BaseCommand):
    help = 'Show the cold storage status'

    def handle(self, *args, **options):
        verbosity = int(options['verbosity'])
        self.unsure_file_copies(verbosity)

    def unsure_file_copies(self, verbosity):
        before = datetime.now() - CONFIDENCE_INTERVAL
        unsure_count = Count('copies', filter=Q(copies__last_checked__lt=before))
        annotated_disks = Disk.objects.annotate(unsure_count=unsure_count)

        self.stdout.write('\nNeed to check the following disks:')

        for disk in annotated_disks:
            if not disk.unsure_count:
                continue

            self.stdout.write(f'- {disk.name} (not sure about {disk.unsure_count} file copies)')

            if verbosity > 1:
                for copy in FileCopy.objects.filter(disk=disk, last_checked__lt=before).select_related('file'):
                    self.stdout.write(f'\t- {copy.file.name}')
