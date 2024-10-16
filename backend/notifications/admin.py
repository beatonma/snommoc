from django.contrib import admin

from common.admin import BaseAdmin
from notifications.models import TaskNotification


@admin.register(TaskNotification)
class TaskNotificationAdmin(BaseAdmin):
    list_display = [
        "started_at",
        "finished_at",
        "complete",
        "failed",
    ]

    ordering = [
        "-started_at",
        "-finished_at",
    ]

    readonly_fields = [
        "content",
        "title",
        "created_on",
        "level",
        "uuid",
        "finished_at",
        "complete",
        "failed",
    ]
