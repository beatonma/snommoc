import logging

from django.http import HttpResponse

from dashboard.views.dashboard import StaffView
from repository.models import Constituency, UnlinkedConstituency
from repository.resolution.constituency import resolve_unlinked_constituency


log = logging.getLogger(__name__)


class ConfirmConstituencyView(StaffView):
    """
    Confirm a link from an UnlinkedConstituency to a canonical Constituency.
    """

    def post(self, request, *args, **kwargs):

        try:
            unlinked = UnlinkedConstituency.objects.get(pk=kwargs.get("unlinked_id"))
            canonical_constituency = Constituency.objects.get(
                parliamentdotuk=kwargs.get("constituency_id")
            )
            resolve_unlinked_constituency(unlinked, canonical=canonical_constituency)
        except Exception as e:
            log.warning(e)
            return HttpResponse(status=400)

        return HttpResponse(status=204)
