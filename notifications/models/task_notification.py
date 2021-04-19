"""

"""

import logging

import uuid as uuid
from functools import wraps

from django.db import models
from django.utils import timezone

from repository.models.mixins import BaseModel
from notifications import permissions

log = logging.getLogger(__name__)


class TaskNotification(BaseModel):
    class Meta:
        permissions = [
            (permissions.VIEW_NOTIFICATION,
             'Can view notifications generated by tasks'),
            (permissions.DISMISS_NOTIFICATION,
             'Can dismiss notifications generated by tasks')
        ]

    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    read = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True, null=True)
    finished_at = models.DateTimeField(null=True)

    complete = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)

    @property
    def finished(self):
        return self.complete or self.failed

    def mark_as_read(self):
        self.read = True
        self.save()

    def mark_as_complete(self):
        self.complete = True
        self.finished_at = timezone.now()
        self.save()

    def mark_as_failed(self, err=None):
        if err:
            self.content = (self.content or '') + '\n' + str(err)

        self.failed = True
        self.finished_at = timezone.now()
        self.save()

    def append(self, content: str):
        self.content = (self.content or '') + '\n' + content
        self.save()

    @classmethod
    def create(cls, content: str, title: str = 'Task notification'):
        n = TaskNotification.objects.create(content=content, title=title)
        n.save()
        return n

    def __str__(self):
        return f'{self.title}'


def task_notification(label):
    """Wrapper for a task. Creates a TaskNotification at start and updates it when task completes or fails."""

    def notification_decoration(func):
        @wraps(func)
        def create_notification(*args, **kwargs):
            notification = TaskNotification.objects.create(title=f'[Starting] {label}')
            notification.save()

            try:
                func(*args, notification=notification, **kwargs)

                notification.title = f'[Finished] {label}'
                notification.mark_as_complete()
            except (Exception, KeyboardInterrupt) as e:
                log.error(e)
                notification.title = f'[Failed] {label}'
                notification.mark_as_failed(err=e)
            finally:
                if not notification.finished:
                    notification.title = f'[Failed] {label}'
                    notification.mark_as_failed()

        return create_notification

    return notification_decoration
