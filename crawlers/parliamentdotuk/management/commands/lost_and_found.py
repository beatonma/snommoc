from django.core.management import BaseCommand

from repository.models import Person, Constituency
from repository.models.houses import HOUSE_OF_COMMONS


class Command(BaseCommand):
    help = 'Detect objects that are missing data they should have. e.g. MPs without a constituency.'
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass


    def _find_homeless_mps(self):
        """Look for MPs who do not have a related Constituency"""
        mps = Person.objects.filter(
            active=True,
            house__name=HOUSE_OF_COMMONS,
            constituency=None,
        )

        self.stdout('MPs with missing constituency:')
        for mp in mps:
            self.stdout(f' [{mp.parliamentdotuk}] {mp.name} has no constituency')

    def _find_memberless_constituencies(self):
        """Look for constituencies that do not have a related MP."""
        constituencies = Constituency.objects.filter(
            end=None, # Constituency currently exists/is not historical
            mp=None,
        )

        self.stdout('Constituencies with missing MP:')
        for constituency in constituencies:
            self.stdout(f'[{constituency.parliamentdotuk}] {constituency.name} {constituency.start}')
