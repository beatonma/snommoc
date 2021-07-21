from django.http import HttpResponse
from django.views.generic.base import View


class PingView(View):
    """Return a simple response to confirm the server is available."""

    def dispatch(self, request, *args, **kwargs):
        return HttpResponse("OK", status=200)
