from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Add many files'

    def add_arguments(self, parser):
        parser.add_argument('disk')
        parser.add_argument('path', nargs='+')
        parser.add_argument('--copy', action='store_true')

    def handle(self, *args, **options):
        for path in options['path']:
            call_command('addfile', options['disk'], path, copy=options['copy'])
