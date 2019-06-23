"""

"""

import logging

from django.contrib import admin

from notifications.models import TaskNotification

log = logging.getLogger(__name__)


@admin.register(TaskNotification)
class TaskNotificationAdmin(admin.ModelAdmin):
    pass
