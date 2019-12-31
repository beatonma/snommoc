"""

"""

import logging

from django.http import (
    HttpResponse,
    Http404,
)

from crawlers.parliamentdotuk.tasks import (
    update_constituencies,
    # update_mps,
)
from dashboard.views.dashboard import BaseDashboardView

log = logging.getLogger(__name__)


class UpdateConstituenciesView(BaseDashboardView):
    def get(self, request, *args, **kwargs):
        follow_pagination = kwargs.get('requirement') != 'debug'
        update_constituencies(follow_pagination=follow_pagination)
        return HttpResponse('OK')


class UpdateMpsView(BaseDashboardView):
    def get(self, request, *args, **kwargs):
        return Http404('Deprecated model!')
        # follow_pagination = kwargs.get('requirement') != 'debug'
        # update_mps(follow_pagination=follow_pagination)
        # return HttpResponse('OK')
