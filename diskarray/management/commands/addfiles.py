from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Add many files'

    def add_arguments(self, parser):
        parser.add_argument('disk')
        parser.add_argument('path', nargs='+')

    def handle(self, *args, **options):
        for path in options['path']:
            call_command('addfile', options['disk'], path)
