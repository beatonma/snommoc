from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views import View
from rest_framework.viewsets import ModelViewSet

from dashboard.views.serializers.task_notifications import TaskNotificationSerializer
from dashboard.views.serializers.unlinked_constituencies import UnlinkedConstituencySerializer
from notifications.models import TaskNotification

from repository.models.constituency import UnlinkedConstituency


def _with_unread_notifications(context: dict):
    context['notifications'] = TaskNotification.objects.order_by('-created_on')[:20]
    context['unlinked_constituencies'] = UnlinkedConstituency.objects.all()
    return context


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
    queryset = UnlinkedConstituency.objects.all()
    serializer_class = UnlinkedConstituencySerializer


class RecentNotificationsViewSet(StaffViewSet):
    queryset = TaskNotification.objects.filter(level__gte=TaskNotification.LEVEL_INFO).order_by('-created_on')[:50]
    serializer_class = TaskNotificationSerializer
