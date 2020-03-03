"""

"""

import logging

from django.http import (
    HttpResponse,
)

from crawlers.parliamentdotuk.tasks import (
    update_constituencies,
)
from crawlers.parliamentdotuk.tasks.membersdataplatform.active_members import update_active_member_details
from crawlers.parliamentdotuk.tasks.membersdataplatform.all_members import update_all_members_basic_info
from dashboard.views.dashboard import BaseDashboardView

log = logging.getLogger(__name__)


class UpdateConstituenciesView(BaseDashboardView):
    def get(self, request, *args, **kwargs):
        follow_pagination = kwargs.get('requirement') != 'debug'
        update_constituencies(follow_pagination=follow_pagination)
        return HttpResponse('OK')


class UpdateMpsView(BaseDashboardView):
    def get(self, request, *args, **kwargs):
        update_all_members_basic_info()
        update_active_member_details()
        return HttpResponse('OK')


class UpdatePartiesView(BaseDashboardView):
    def get(self, request, *args, **kwargs):
        from repository.tasks import init_parties
        init_parties()
        return HttpResponse('OK')


class RebuildAllView(BaseDashboardView):
    def get(self, request, *args, **kwargs):
        from crawlers.parliamentdotuk.tasks import rebuild_all_data

        rebuild_all_data()
