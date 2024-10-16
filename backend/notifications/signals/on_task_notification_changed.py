from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import TaskNotification
from notifications.tasks.push_notification import push_notification


@receiver(
    post_save,
    sender=TaskNotification,
    dispatch_uid="send_notification_on_tasknotification_changed",
)
def send_notification_on_tasknotification_changed(
    sender, instance: TaskNotification, using, **kwargs
):
    push_notification(instance.title, instance.content)
