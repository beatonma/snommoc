from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from notifications.models import TaskNotification


class DashboardView(View):
    def get(self, request):
        return render(
            request,
            'staff-dashboard.html',
            {
                'notifications': TaskNotification.objects.filter(read=False)
            }
        )
