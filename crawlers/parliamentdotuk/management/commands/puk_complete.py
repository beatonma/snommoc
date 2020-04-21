"""

"""

from django.core.management import BaseCommand

from crawlers.parliamentdotuk.tasks.membersdataplatform import complete_update


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        complete_update.delay()
