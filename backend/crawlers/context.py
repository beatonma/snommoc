import logging
from functools import wraps

from celery import shared_task
from crawlers.network import JsonCache, json_cache
from notifications.models import TaskNotification
from notifications.models.task_notification import task_notification
from requests import Session


class TaskContext:
    def __init__(
        self,
        cache: JsonCache | None,
        notification: TaskNotification | None,
        session: Session | None = None,
        force_update: bool = False,
        skip_items: int = 0,
        max_items: int = None,
        items_per_page: int | None = None,
    ):
        self.failed = False
        self.complete = False
        self.notification = notification
        self.cache = cache
        self.session = session or Session()
        self.force_update = force_update
        self.skip_items = skip_items
        self.max_items = max_items
        self.items_per_page = items_per_page

    def limit_reached(self, item_count: int) -> bool:
        """Return True if item_count exceeds task limits"""
        if (max_items := self.max_items) is not None and item_count >= max_items:
            self.info(f"Task max_items={max_items} limit reached.")
            return True
        return False

    def is_finished(self) -> bool:
        return self.failed or self.complete

    def info(self, content: str):
        if notification := self.notification:
            notification.info(content)

    def warning(self, content: str):
        if notification := self.notification:
            notification.warning(content)

    def error(self, error: Exception, content: str):
        self.failed = True
        if notification := self.notification:
            notification.error(error, content)

    def mark_as_complete(self):
        self.complete = True
        if notification := self.notification:
            notification.mark_as_complete()

    def mark_as_failed(self, err=None):
        self.failed = True
        if notification := self.notification:
            notification.mark_as_failed(err)


def task_context(
    *,
    cache_name: str,
    label: str = None,
    cache_ttl: int = None,
    log_level: int = logging.INFO,
):
    def task_decoration(func):

        @shared_task
        @json_cache(name=cache_name, ttl_seconds=cache_ttl)
        @task_notification(
            label=label or func.__name__.replace("_", " ").capitalize(),
            level=log_level,
        )
        @wraps(func)
        def wrapper(*args, cache: JsonCache, notification: TaskNotification, **kwargs):
            context = kwargs.pop(
                "context",  # If context already active, use that.
                TaskContext(
                    cache=cache,
                    notification=notification,
                    # TaskCommand kwargs
                    force_update=kwargs.pop("force_update", False),
                    skip_items=kwargs.pop("skip_items", 0),
                    max_items=kwargs.pop("max_items", None),
                ),
            )
            func(*args, context=context, **kwargs)

        return wrapper

    return task_decoration
