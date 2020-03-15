"""

"""

import logging

from rest_framework import viewsets

from api.views.decorators import api_key_required

log = logging.getLogger(__name__)


class KeyRequiredViewSet(viewsets.ReadOnlyModelViewSet):
    """Base class for any ViewSet that requires a key/authorised user."""
    @api_key_required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
