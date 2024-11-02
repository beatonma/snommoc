from api.views.decorators import api_key_required
from rest_framework import viewsets
from util.cleanup import Deprecated


class KeyRequiredViewSet(Deprecated, viewsets.ReadOnlyModelViewSet):
    """Base class for any ViewSet that requires a key/authorised user."""

    @api_key_required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
