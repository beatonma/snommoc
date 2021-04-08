from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'notifications'

    def ready(self):
        import notifications.signals.on_task_notification_changed  # noqa
