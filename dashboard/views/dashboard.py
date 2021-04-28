from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views import View
from rest_framework.viewsets import ModelViewSet

from dashboard.views.serializers.task_notifications import TaskNotificationSerializer
from dashboard.views.serializers.unlinked_constituencies import UnlinkedConstituencySerializer
from notifications.models import TaskNotification

from repository.models.constituency import UnlinkedConstituency


class StaffView(UserPassesTestMixin, View):
    """Dashboard is only viewable by staff accounts."""

    def test_func(self):
        return self.request.user.is_staff

    class Meta:
        abstract = True


class StaffViewSet(UserPassesTestMixin, ModelViewSet):
    """Dashboard is only viewable by staff accounts."""

    def test_func(self):
        return self.request.user.is_staff

    class Meta:
        abstract = True


class DashboardView(StaffView):
    def get(self, request):
        return render(
            request,
            'dashboard.html',
        )


class UnlinkedConstituencyViewSet(StaffViewSet):
    queryset = UnlinkedConstituency.objects.all().order_by('name', 'election__date')
    serializer_class = UnlinkedConstituencySerializer


class RecentNotificationsViewSet(StaffViewSet):
    queryset = TaskNotification.objects.filter(level__gte=TaskNotification.LEVEL_INFO).order_by('-created_on')[:50]
    serializer_class = TaskNotificationSerializer
