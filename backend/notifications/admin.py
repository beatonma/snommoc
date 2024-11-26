from common.admin import BaseAdmin
from django.contrib import admin
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
        "created_at",
        "level",
        "uuid",
        "finished_at",
        "complete",
        "failed",
    ]
