from django.core.management import BaseCommand

from repository.tasks.consistency import check_consistency


class Command(BaseCommand):
    def handle(self, *args, **options):
        check_consistency()
