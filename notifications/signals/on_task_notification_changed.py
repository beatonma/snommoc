from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import TaskNotification


@receiver(
    post_save,
    sender=TaskNotification,
    dispatch_uid='send_notification_on_tasknotification_changed'
)
def send_notification_on_tasknotification_changed(sender, instance: TaskNotification, using, **kwargs):
    try:
        from bmanotify import EventNotifier

    except ImportError:
        return

    try:
        EventNotifier(
            title=instance.title,
            body=instance.content,
            tag='snommoc.org',
        ).send()
    except Exception:
        pass
