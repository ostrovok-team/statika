from logging import getLogger, StreamHandler
from django.conf import settings
from django.core.management.base import BaseCommand
from statika import build


class Command(BaseCommand):
    help = 'Builds static bundles by python-statika'

    def handle(self, *args, **options):
        getLogger('statika').addHandler(StreamHandler())
        build(settings.STATIKA_BUNDLES)
