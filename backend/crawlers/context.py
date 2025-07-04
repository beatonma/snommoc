import logging
from functools import wraps

from celery import shared_task
from common.cache import invalidate_cache
from crawlers.caches import API_VIEW_CACHE
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
        historic: bool = False,
        skip_items: int = 0,
        max_items: int = None,
        items_per_page: int | None = None,
        item_id: int | None = None,
        follow_pagination: bool = True,
    ):
        """

        Args:
            cache: JsonCache used to avoid repeated network requests.
            notification: TaskNotification for tracking task progress and reporting any issues.
            session: Session for network requests.
            force_update: If True, tasks should update data from the source even if we already have a local version.
            historic: If True, tasks should update historical data: i.e. Anything that is not related to the current parliamentary session.
            skip_items: Skip processing of the first n items.
            max_items: Stop processing after this many items.
            items_per_page: Ask API pagination to return this many items.
            item_id: Only fetch data for a single item.
            follow_pagination: If false, only process the first page of results.
        """
        self.failed = False
        self.complete = False
        self.notification = notification
        self.cache = cache
        self.session = session or Session()
        self.force_update = force_update
        self.historic = historic
        self.skip_items = skip_items
        self.max_items = max_items
        self.items_per_page = items_per_page
        self.item_id = item_id
        self.follow_pagination = follow_pagination

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
    items_per_page: int | None = None,
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
            try:
                context = kwargs.pop(
                    "context",  # If context already active, use that.
                    TaskContext(
                        cache=cache,
                        notification=notification,
                        # TaskCommand kwargs
                        historic=kwargs.pop("historic", False),
                        force_update=kwargs.pop("force_update", False),
                        skip_items=kwargs.pop("skip_items", 0),
                        max_items=kwargs.pop("max_items", None),
                        items_per_page=kwargs.pop("items_per_page", items_per_page),
                        item_id=kwargs.pop("item_id", None),
                    ),
                )
                func(*args, context=context, **kwargs)

            finally:
                # When task completes, invalidate API cache of stale data.
                invalidate_cache(API_VIEW_CACHE)

        return wrapper

    return task_decoration
