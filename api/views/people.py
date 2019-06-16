from django.http import (
    JsonResponse,
    Http404,
    HttpResponseBadRequest,
)
from django.views import View

from api import contract
from api.views.decorators import api_key_required
from repository.models import Mp


def remove_none(obj):
    remove_keys = []
    for key, value in obj.items():
        if not value:
            remove_keys.append(key)

    for key in remove_keys:
        del obj[key]


class GetMpView(View):
    """/get_mp"""
    @api_key_required
    def dispatch(self, request, *args, **kwargs):
        query = {
            contract.THEYWORKFORYOU_ID: request.GET.get(contract.THEYWORKFORYOU_ID),
            contract.PARLIAMENTDOTUK_ID: request.GET.get(contract.PARLIAMENTDOTUK_ID)
        }
        remove_none(query)
        if not query:
            return HttpResponseBadRequest(
                'Please provide an ID value for '
                f'{contract.THEYWORKFORYOU_ID} or {contract.PARLIAMENTDOTUK_ID}')

        try:
            mp = Mp.objects.get(**query)
            return JsonResponse(
                mp.to_json()
            )
        except Mp.DoesNotExist:
            return Http404()
