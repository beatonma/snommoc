"""

"""

import logging

from rest_framework import viewsets

from api.serializers import (
    MpSerializer,
    ConstituencySerializer,
    PartySerializer,
)
from api.views.decorators import api_key_required
from repository.models import (
    Mp,
    Constituency,
    Party,
)

log = logging.getLogger(__name__)


class KeyRequiredViewSet(viewsets.ReadOnlyModelViewSet):
    @api_key_required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PartyViewSet(KeyRequiredViewSet):
    """Political party"""
    queryset = Party.objects.all()
    serializer_class = PartySerializer


class ConstituencyViewSet(KeyRequiredViewSet):
    """Parliamentary constituency"""
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer


class MpViewSet(KeyRequiredViewSet):
    """Member of Parliament"""
    queryset = Mp.objects.all()
    serializer_class = MpSerializer
