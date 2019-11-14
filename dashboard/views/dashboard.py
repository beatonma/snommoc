from django.db.models import Q
from django.shortcuts import render
from django.views import View

from notifications.models import TaskNotification
from repository.models import (
    Mp,
    Constituency,
    Party,
)


def with_unread_notifications(context: dict):
    context['notifications'] = TaskNotification.objects.filter(read=False)
    return context


class DashboardView(View):
    def get(self, request):
        return render(
            request,
            'staff-dashboard.html',
            with_unread_notifications({
                'mp_count': Mp.objects.count(),
                'constituency_count': Constituency.objects.count(),
                'party_count': Party.objects.count(),
            })
        )


class MpDashboardView(View):
    def get(self, request, *args, **kwargs):
        if kwargs.get('requirement') == 'active':
            mps = Mp.objects.prefetch_related('party') \
                .order_by('person__family_name') \
                .exclude(constituency__isnull=True)
        else:
            mps = Mp.objects.prefetch_related('party') \
                .order_by('person__family_name')
        return render(
            request,
            'dashboard-all-mps.html',
            with_unread_notifications({
                'items': mps,
            })
        )


class ConstituencyDashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'dashboard-all-constituencies.html',
            with_unread_notifications({
                'items': Constituency.objects.order_by('name'),
            })
        )


class PartyDashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'dashboard-all-parties.html',
            with_unread_notifications({
                'items': Party.objects.order_by('name'),
            })
        )
