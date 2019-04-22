from django.core.management.base import BaseCommand, CommandError

from finder.models import Folder


class Command(BaseCommand):
    help = 'Delete files and folders'

    def add_arguments(self, parser):
        parser.add_argument('folder_id', type=int)

    def handle(self, *args, **options):
        self.stdout.write('---')

        folder = Folder.objects.get(id=options['folder_id'])
        self.delete(folder)

    def delete(self, folder):
        self.stdout.write('Folder = %s' % folder)
        if input('Continue? ')[:1].lower() != 'y':
            raise CommandError('Aborted by user')

        subdirectories = folder.subdirectories.all()
        for sd in subdirectories:
            self.delete(sd)

        files = folder.files.all()
        self.stdout.write('Files: %d' % files.count())
        for file in files:
            self.delete_file(folder, file)

        folder.delete()

    def delete_file(self, folder, file):
        self.stdout.write('- %s' % file)
        file.folders.remove(folder)
        if file.folders.count():
            self.stdout.write('  (retaining)')
        else:
            self.stdout.write('  (deleting)')
            for copy in file.copies.all():
                self.stdout.write('  - %s' % copy)
                copy.delete()
            file.delete()
