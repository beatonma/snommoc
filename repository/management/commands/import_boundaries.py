"""
Sample data:
https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(BDY_PCON%2CDEC_2018)
"""

import logging

from django.core.management import BaseCommand

from repository.tasks.construct_constituency_boundaries import (
    import_boundaries_from_file,
)

log = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'file'
        )

    def handle(self, *args, **options):
        filepath = options['file']
        log.info(f'Importing constituency boundaries from {filepath}')
        imported_count = import_boundaries_from_file(options['file'])

        log.info(f'Import complete: found {imported_count} boundaries.')
