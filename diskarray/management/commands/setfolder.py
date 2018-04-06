from django.core.management.base import BaseCommand

from diskarray.models import File
from finder.models import Folder


class Command(BaseCommand):
    help = 'Put files in a folder'

    def add_arguments(self, parser):
        parser.add_argument('folder_id', type=int)

    def handle(self, *args, **options):
        self.stdout.write('---')

        folder = Folder.objects.get(id=options['folder_id'])
        self.stdout.write('Folder = %s' % folder)

        files = File.objects.filter(folders=None)
        self.stdout.write('Files: %d' % files.count())

        for file in files:
            self.stdout.write('- %s' % file)
            file.folders.add(folder)
