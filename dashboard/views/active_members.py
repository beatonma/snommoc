import logging

from django.http import JsonResponse, HttpResponse

from dashboard.views.dashboard import StaffView
from repository.models import Person
from repository.resolution import get_active_members

log = logging.getLogger(__name__)


class ActiveMembersView(StaffView):
    def get(self, request, *args, **kwargs):
        members = get_active_members()

        return JsonResponse(
            {
                "members": [
                    {
                        "parliamentdotuk": m.pk,
                        "name": m.name,
                        "wikipedia": m.wikipedia,
                        "house": m.house.name,
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
