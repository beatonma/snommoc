import logging

from dashboard.views.dashboard import StaffView
from django.http import HttpResponse, JsonResponse
from repository.models import Person

log = logging.getLogger(__name__)


class ActiveMembersView(StaffView):
    def get(self, request, *args, **kwargs):
        members = Person.objects.active()

        return JsonResponse(
            {
                "members": [
                    {
                        "parliamentdotuk": m.pk,
                        "name": m.name,
                        "simple_name": f"{m.given_name} {m.family_name}",
                        "wikipedia": m.wikipedia,
                        "party": m.party.name if m.party else None,
                        "house": m.house.name,
                        "has_portrait": m.portrait_fullsize_url is not None,
                    }
                    for m in members
                ]
            }
        )

    def post(self, request, *args, **kwargs):
        params = request.POST
        member_id = params.get("member_id")
        wikipedia = params.get("wikipedia")

        try:
            if wikipedia:
                person = Person.objects.get(pk=int(member_id))
                person.wikipedia = wikipedia
                person.save()
        except Exception as e:
            log.warning(e)
            return HttpResponse(status=400)

        return HttpResponse(status=204)
