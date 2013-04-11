from logging import getLogger, StreamHandler
from django.conf import settings
from django.core.management.base import BaseCommand
from statika import build


class Command(BaseCommand):
    help = 'Builds static bundles by python-statika'

    def handle(self, *args, **options):
        getLogger('statika').addHandler(StreamHandler())
        bundles = [
            settings.MEDIA_ROOT + '/js/bakkota.js',
            settings.MEDIA_ROOT + '/css/bakkota.css',
        ]
        build(bundles)
