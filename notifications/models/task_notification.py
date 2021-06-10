"""

"""

import logging

import uuid as uuid
from functools import wraps

from django.db import models
from django.utils import timezone

from notifications import permissions
from util.time import get_now

log = logging.getLogger(__name__)


class TaskNotification(models.Model):
    class Meta:
        permissions = [
            (
                permissions.VIEW_NOTIFICATION,
                "Can view notifications generated by tasks",
            ),
            (
                permissions.DISMISS_NOTIFICATION,
                "Can dismiss notifications generated by tasks",
            ),
        ]

    LEVEL_VERBOSE = 0
    LEVEL_DEBUG = 1
    LEVEL_INFO = 2
    LEVEL_WARN = 3

    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    read = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True, null=True)
    finished_at = models.DateTimeField(null=True)

    complete = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)

    level = models.PositiveSmallIntegerField(default=LEVEL_INFO)

    @property
    def finished(self):
        return self.complete or self.failed

    def mark_as_read(self):
        self.read = True
        self.save()

    def mark_as_complete(self):
        if self.failed:
            log.warning(
                "TaskNotification.mark_as_complete called on task already marked as FAILED"
            )
            return

        if self.complete:
            log.warning(
                "TaskNotification.mark_as_complete called on task already marked as complete"
            )
            return

        self.complete = True
        self.finished_at = get_now()
        self.save()

    def mark_as_failed(self, err=None):
        if err:
            self.content = (self.content or "") + "\n" + str(err)

        self.failed = True
        self.finished_at = get_now()
        self.save()

    def append(self, content: str):
        if self.finished:
            log.warning("Task marked as finished but still being appended to")
        log.info(content)
        self.content = (self.content or "") + "\n" + content
        self.save()

    @classmethod
    def create(cls, content: str, title: str = "Task notification"):
        n = TaskNotification.objects.create(content=content, title=title)
        n.save()
        return n

    def __str__(self):
        return f"{self.title}"


def task_notification(label, level=TaskNotification.LEVEL_INFO):
    """Wrapper for a task. Creates a TaskNotification at start and updates it when task completes or fails."""

    def notification_decoration(func):
        @wraps(func)
        def create_notification(*args, **kwargs):
            is_root_task = "notification" not in kwargs

            if not is_root_task:
                notification = kwargs["notification"]
            else:
                notification = TaskNotification.objects.create(
                    title=f"{label}", level=level
                )
                notification.save()
                kwargs["notification"] = notification

            try:
                func(*args, **kwargs)
                if is_root_task:
                    notification.mark_as_complete()

            except (Exception, KeyboardInterrupt) as e:
                log.error(e)
                notification.mark_as_failed(err=e)

            finally:
                if is_root_task and not notification.finished:
                    notification.mark_as_failed()

        return create_notification

    return notification_decoration
