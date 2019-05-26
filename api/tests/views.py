from django.http import HttpResponse
from django.views import View

from api.views.decorators.api_key_required import api_key_required


class ExampleView(View):
    @api_key_required
    def dispatch(self, request, *args, **kwargs):
        return HttpResponse('OK')
