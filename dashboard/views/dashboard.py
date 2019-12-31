from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import (
    Count,
    QuerySet,
)
from django.http import Http404
from django.shortcuts import render
from django.views import View

from notifications.models import TaskNotification
from repository.models import (
    Constituency,
    # Mp,
    Party,
)


def with_unread_notifications(context: dict):
    context['notifications'] = TaskNotification.objects.filter(read=False)
    return context


class BaseDashboardView(UserPassesTestMixin, View):
    """Dashboard is only viewable by staff accounts."""

    def test_func(self):
        return self.request.user.is_staff

    class Meta:
        abstract = True


class DashboardView(BaseDashboardView):
    def get(self, request):
        return render(
            request,
            'staff-dashboard.html',
            with_unread_notifications({
                # 'mp_count': Mp.objects.count(),
                'constituency_count': Constituency.objects.count(),
                'party_count': Party.objects.count(),
            })
        )


class MpDashboardView(BaseDashboardView):
    def get(self, request, *args, **kwargs):
        return Http404('Deprecated model')
        # if kwargs.get('requirement') == 'active':
        #     # Only show MPs that are attached to an extant constituency
        #     # i.e. they are a current MP, not just historic.
        #     mps = Mp.objects.all()
        #     active_mp_ids = [mp.id for mp in mps if hasattr(mp, 'constituency') and mp.constituency.is_extant]
        #     mps: QuerySet = Mp.objects.prefetch_related('party') \
        #         .filter(id__in=active_mp_ids) \
        #         .order_by('person__family_name')
        #
        # else:
        #     mps = Mp.objects.prefetch_related('party') \
        #         .order_by('person__family_name')
        # return render(
        #     request,
        #     'dashboard-all-mps.html',
        #     with_unread_notifications({
        #         'items': mps,
        #     })
        # )


class ConstituencyDashboardView(BaseDashboardView):
    def get(self, request, *args, **kwargs):
        if kwargs.get('requirement') == 'active':
            constituencies = Constituency.objects.exclude(end__isnull=True).order_by('name')
        else:
            constituencies = Constituency.objects.order_by('name')
        return render(
            request,
            'dashboard-all-constituencies.html',
            with_unread_notifications({
                'items': constituencies,
            })
        )


class PartyDashboardView(BaseDashboardView):
    def get(self, request, *args, **kwargs):
        if kwargs.get('requirement') == 'active':
            parties = Party.objects.annotate(mp_population=Count('mps')) \
                .exclude(mp_population=0) \
                .order_by('-mp_population')
        else:
            parties = Party.objects.order_by('name')
        return render(
            request,
            'dashboard-all-parties.html',
            with_unread_notifications({
                'items': parties,
            })
        )
