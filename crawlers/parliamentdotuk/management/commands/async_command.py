"""

"""

import logging

from django.core.management import BaseCommand

log = logging.getLogger(__name__)


class AsyncCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-async',
            action='store_true',
            help='Pass update task to Celery.',
        )

    def handle_async(self, func, *args, **options):
        """
        Call from handle, passing the function along with the received options.

        e.g.
        def handle(self, *args, **options):
            self.handle_async(myfunc, *args, **options)
        """
        if options['async']:
            func.delay()
        else:
            func()
