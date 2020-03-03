from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import (
    QuerySet,
)
from django.shortcuts import render
from django.views import View

from notifications.models import TaskNotification
from repository.models import (
    Constituency,
    Party,
    Person,
)
from repository.models.constituency import UnlinkedConstituency
from repository.models.houses import (
    HOUSE_OF_COMMONS,
    HOUSE_OF_LORDS,
)


def with_unread_notifications(context: dict):
    context['notifications'] = TaskNotification.objects.filter(read=False)
    context['unlinked_constituencies'] = UnlinkedConstituency.objects.all().count()
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
                'mp_count': Person.objects.count(),
                'constituency_count': Constituency.objects.count(),
                'party_count': Party.objects.count(),
            })
        )


class MemberDashboardView(BaseDashboardView):
    def get(self, request, *args, **kwargs):
        if kwargs.get('requirement') == 'active':
            members: QuerySet = Person.objects.filter(
                active=True,
            ).prefetch_related('party') \
                .order_by('family_name')
        else:
            members = Person.objects.prefetch_related('party') \
                .order_by('family_name')
        return render(
            request,
            'dashboard-all-members.html',
            with_unread_notifications({
                'items': members,
            })
        )


class MpDashboardView(BaseDashboardView):
    def get(self, request, *args, **kwargs):
        if kwargs.get('requirement') == 'active':
            mps: QuerySet = Person.objects.filter(
                house__name=HOUSE_OF_COMMONS,
                active=True,
            ).prefetch_related('party') \
                .order_by('family_name')
        else:
            mps = Person.objects.filter(
                house__name=HOUSE_OF_COMMONS,
            ).prefetch_related('party') \
                .order_by('family_name')
        return render(
            request,
            'dashboard-all-mps.html',
            with_unread_notifications({
                'items': mps,
            })
        )


class LordDashboardView(BaseDashboardView):
    def get(self, request, *args, **kwargs):
        if kwargs.get('requirement') == 'active':
            lords: QuerySet = Person.objects.filter(
                house__name=HOUSE_OF_LORDS,
                active=True,
            ).prefetch_related('party') \
                .order_by('family_name')
        else:
            lords = Person.objects.filter(
                house__name=HOUSE_OF_LORDS,
            ).prefetch_related('party') \
                .order_by('family_name')
        return render(
            request,
            'dashboard-all-lords.html',
            with_unread_notifications({
                'items': lords,
            })
        )


class ConstituencyDashboardView(BaseDashboardView):
    def get(self, request, *args, **kwargs):
        if kwargs.get('requirement') == 'active':
            constituencies = Constituency.objects.filter(mp__active=True).order_by('name')
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
            mps = Person.objects.filter(active=True, house__name=HOUSE_OF_COMMONS).prefetch_related('party')
            active_parties = [mp.party.id for mp in mps]

            parties = Party.objects.filter(id__in=active_parties)

            # parties = Party.objects.annotate(mp_population=Count('people')) \
            #     .exclude(mp_population=0) \
            #     .order_by('-mp_population')
        else:
            parties = Party.objects.order_by('name')
        return render(
            request,
            'dashboard-all-parties.html',
            with_unread_notifications({
                'items': parties,
            })
        )
