from django.contrib import admin

from notifications.models import TaskNotification


@admin.register(TaskNotification)
class TaskNotificationAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "started_at",
        "finished_at",
        "finished",
    ]

    ordering = [
        "-started_at",
        "-finished_at",
    ]
