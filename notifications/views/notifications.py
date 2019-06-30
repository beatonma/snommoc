"""

"""

import logging

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)
from django.views import View

from notifications.models import TaskNotification
from notifications import permissions

log = logging.getLogger(__name__)


VIEW_PENDING_NOTIFICATIONS = 'pending_notifications_view'
VIEW_CREATE_NOTIFICATION = 'create_notification_view'
VIEW_DISMISS_NOTIFICATION = 'dismiss_notification_view'


class PendingNotificationsView(UserPassesTestMixin, View):
    def get(self, request):
        notifications = [x.__str__() for x in TaskNotification.objects.all()]
        html = '<br/>'.join(notifications)

        return HttpResponse(html)

    def test_func(self):
        return self.request.user.has_perm(
            f'notifications.{permissions.VIEW_NOTIFICATION}')


class CreateNotificationView(UserPassesTestMixin, View):
    def get(self, request):
        n = TaskNotification.create('content')
        return HttpResponse(n)

    def test_func(self):
        return self.request.user.has_perm(
            f'notifications.{permissions.CREATE_NOTIFICATION}')


class DismissNotificationView(UserPassesTestMixin, View):
    def get(self, request):
        uuid = request.GET.get('uuid')
        if not uuid:
            return HttpResponseBadRequest('id required')
        try:
            n = TaskNotification.objects.get(uuid=uuid)
            n.delete()
        except TaskNotification.DoesNotExist:
            return HttpResponseNotFound()

    def test_func(self):
        return self.request.user.has_perm(
            f'notifications.{permissions.DISMISS_NOTIFICATION}')
