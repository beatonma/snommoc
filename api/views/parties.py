from django.http import JsonResponse
from django.views import View

from api import contract
from api.views.decorators import api_key_required
from repository.models import Party

VIEW_GET_PARTIES = 'get_parties_view'


class GetPartiesView(View):
    """/get_parties"""
    @api_key_required
    def dispatch(self, request, *args, **kwargs):
        parties = Party.objects.all()
        return JsonResponse({
            contract.PARTIES: [p.to_json() for p in parties]
        })
