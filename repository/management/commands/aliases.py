"""

"""

import logging

from django.core.management import BaseCommand

from repository.models import BillSponsor
from repository.models.person import PersonAlsoKnownAs

log = logging.getLogger(__name__)


def _update_sponsor_aliases():
    # Bill sponsors are created by name lookup which may be represented differently
    # (abbreviated or whatever) than how we normally reference them. This command
    # will check for any unlinked sponsors and try to match them with a Person.

    unlinked_sponsors = BillSponsor.objects.filter(person=None)
    if unlinked_sponsors.count() == 0:
        log.info('All sponsors are already linked!')
        return
    else:
        log.info(f'Attempting to link {unlinked_sponsors.count()} sponsors...')

    for sponsor in unlinked_sponsors:
        try:
            alias = PersonAlsoKnownAs.objects.get(alias=sponsor.name)
            sponsor.person = alias.person
            sponsor.save()

            log.info(f'Linked sponsor name={sponsor.name} -> person={alias.person}')

        except PersonAlsoKnownAs.DoesNotExist:
            pass

    unlinked_sponsors = BillSponsor.objects.filter(person=None)
    if unlinked_sponsors.count() == 0:
        log.info('All sponsors are now linked!')
    else:
        log.info(f'{unlinked_sponsors.count()} sponsors are still unlinked:')
        for sponsor in unlinked_sponsors:
            log.info(f'  "{sponsor.name}"')

        log.info('Please create a PersonAlsoKnownAs instance for these names '
                 'and re-run the command so they can be linked correctly.')


class Command(BaseCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        _update_sponsor_aliases()
