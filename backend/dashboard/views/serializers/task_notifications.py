from rest_framework import serializers

from notifications.models import TaskNotification


class TaskNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskNotification
        fields = [
            'title',
            'content',
            'complete',
            'failed',
            'created_on',
            'finished_at',
            'level',
        ]
