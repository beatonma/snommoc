"""

"""

import logging

from django.core.management import BaseCommand

log = logging.getLogger(__name__)


class AsyncCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-instant',
            action='store_true',
            default=False,
            help='Run the task synchronously.',
        )

    def handle_async(self, func, *args, **options):
        """
        Call from handle, passing the function along with the received options.

        e.g.
        def handle(self, *args, **options):
            self.handle_async(myfunc, *args, **options)
        """
        if options['instant']:
            log.info(f'Launching function `{func}` synchronously.')
            func()
        else:
            log.info(f'Dispatching function `{func}` to worker.')
            func.delay()
