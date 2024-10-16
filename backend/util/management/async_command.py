import logging

from django.core.management import BaseCommand

log = logging.getLogger(__name__)


class AsyncCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-sync",
            action="store_true",
            default=False,
            help="Run the task synchronously.",
        )

        parser.add_argument(
            "-force",
            action="store_true",
            default=False,
            help=(
                "Tell the task not to skip the update of any items that we "
                "already know about."
            ),
        )

    def handle_async(self, func, func_kwargs=None, **command_options):
        """Call from handle(), passing the function along with the received options.

        e.g.
        def handle(self, *args, **options):
            self.handle_async(myfunc, func_kwargs={'whatever': True}, **command_options)

        Any arguments for the func should be in func_kwargs, not command_options.
        """
        if func_kwargs is None:
            func_kwargs = dict()

        assert hasattr(func, "delay"), (
            "AsyncCommand.handle_async received a function that is not registered"
            f"as a task: {func.__name__}"
        )

        # Inject -force management argument to the receiving task as force_update.
        func_kwargs["force_update"] = command_options.get("force") or None

        if command_options["sync"]:
            log.info(
                f"Launching function `{func}` synchronously with kwargs={func_kwargs}."
            )
            func(**func_kwargs)
        else:
            log.info(
                f"Dispatching function `{func}` to worker with kwargs={func_kwargs}."
            )
            func.delay(**func_kwargs)
