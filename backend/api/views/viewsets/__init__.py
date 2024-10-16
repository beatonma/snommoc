from rest_framework import (
    filters,
    viewsets,
)

from api.views.decorators import api_key_required


class KeyRequiredViewSet(viewsets.ReadOnlyModelViewSet):
    """Base class for any ViewSet that requires a key/authorised user."""

    @api_key_required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class Searchable:
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = []
