import logging

from django.core.management import BaseCommand

log = logging.getLogger(__name__)


class TaskCommand(BaseCommand):
    """Use with `@task_context`-decorated tasks to correctly handle arguments"""

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

        parser.add_argument(
            "--skip_items", type=int, default=0, help="Skip the first items of a task."
        )
        parser.add_argument(
            "--max_items",
            type=int,
            default=None,
            help="Stop a task after processing this many items.",
        )

    def handle_async(self, func, func_kwargs: dict | None = None, **command_options):
        """Call from handle(), passing the function along with the received options.

        e.g.
        def handle(self, *args, **options):
            self.handle_async(myfunc, func_kwargs={'whatever': True}, **command_options)

        Any arguments for the func should be in func_kwargs, not command_options.
        """

        assert hasattr(func, "delay"), (
            "AsyncCommand.handle_async received a function that is not registered "
            f"as a task: {func.__name__}"
        )

        if func_kwargs is None:
            func_kwargs = dict()

        sync = command_options.pop("sync")

        # Inject management arguments to the receiving task context.
        func_kwargs["force_update"] = command_options.pop("force")
        func_kwargs["skip_items"] = command_options.pop("skip_items", 0)
        func_kwargs["max_items"] = command_options.pop("max_items", None)

        if sync:
            log.info(
                f"Launching function `{func}` synchronously with kwargs={func_kwargs}."
            )
            func(**func_kwargs)
        else:
            log.info(
                f"Dispatching function `{func}` to worker with kwargs={func_kwargs}."
            )
            func.delay(**func_kwargs)
