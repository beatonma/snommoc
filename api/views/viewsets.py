"""

"""

import logging

from rest_framework import viewsets

from api.serializers import (
    ConstituencySerializer,
    InlineConstituencySerializer,
    InlineMemberSerializer,
    InlinePartySerializer,
    MemberSerializer,
    PartySerializer,
)
from api.views.decorators import api_key_required
from repository.models import (
    Constituency,
    Party,
    Person,
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


class MemberViewSet(KeyRequiredViewSet):
    """Member of Parliament"""
    queryset = Person.objects.all() \
        .prefetch_related('party', 'constituency')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MemberSerializer
        else:
            return InlineMemberSerializer
