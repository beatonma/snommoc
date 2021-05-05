import logging

from django.http import HttpResponse
from django.utils import timezone

from dashboard.views.dashboard import StaffView
from repository.models import Constituency, UnlinkedConstituency
from repository.resolution.constituency import resolve_unlinked_constituency
from surface.models import (
    FeaturedPerson,
    FeaturedBill,
    FeaturedCommonsDivision,
    FeaturedLordsDivision,
)
from surface.tasks import update_zeitgeist


log = logging.getLogger(__name__)


class _ToggleFeaturedView(StaffView):
    """
    Feature/un-feature a target object of type [model].
    """

    model = None

    def post(self, request, *args, **kwargs):
        parliamentdotuk = kwargs.get("id")
        try:
            self.model.objects.update_or_create(
                target_id=parliamentdotuk,
                defaults={
                    "start": timezone.now().date(),
                },
            )
        except Exception as e:
            log.warning(e)
            return HttpResponse(status=400)

        update_zeitgeist()

        return HttpResponse(status=204)

    def delete(self, request, *args, **kwargs):
        parliamentdotuk = kwargs.get("id")

        try:
            obj = self.model.objects.get(target_id=parliamentdotuk)
            obj.delete()
        except Exception as e:
            log.warning(e)
            return HttpResponse(status=404)

        update_zeitgeist()

        return HttpResponse(status=204)


class ToggleFeaturedMemberView(_ToggleFeaturedView):
    model = FeaturedPerson


class ToggleFeaturedBillView(_ToggleFeaturedView):
    model = FeaturedBill


class ToggleFeaturedCommonsDivisionView(_ToggleFeaturedView):
    model = FeaturedCommonsDivision


class ToggleFeaturedLordsDivisionView(_ToggleFeaturedView):
    model = FeaturedLordsDivision


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
