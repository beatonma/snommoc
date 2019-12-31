"""

"""

import logging

from rest_framework import viewsets

from api.serializers import (
    # MpSerializer,
    ConstituencySerializer,
    PartySerializer,
    # InlineMpSerializer,
    InlineConstituencySerializer,
    InlinePartySerializer,
)
from api.views.decorators import api_key_required
from repository.models import (
    # Mp,
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

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PartySerializer
        else:
            return InlinePartySerializer


class ConstituencyViewSet(KeyRequiredViewSet):
    """Parliamentary constituency"""
    queryset = Constituency.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ConstituencySerializer
        else:
            return InlineConstituencySerializer


# class MpViewSet(KeyRequiredViewSet):
#     """Member of Parliament"""
#     queryset = Mp.objects.all().prefetch_related('party', 'constituency')
#
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return MpSerializer
#         else:
#             return InlineMpSerializer
