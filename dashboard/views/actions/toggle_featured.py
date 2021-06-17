import logging

from django.http import HttpResponse

from dashboard.views.dashboard import StaffView
from surface.models import (
    FeaturedBill,
    FeaturedPerson,
    FeaturedCommonsDivision,
    FeaturedLordsDivision,
)
from surface.tasks import update_zeitgeist
from util.time import get_today


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
                    "start": get_today(),
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
