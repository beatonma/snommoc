"""

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
        import_boundaries_from_file(options['file'])
