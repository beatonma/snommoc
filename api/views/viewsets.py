"""

"""

import logging

from rest_framework import viewsets

from api.serializers import (
    ConstituencySerializer,
    InlineConstituencySerializer,
    InlineMemberSerializer,
    InlinePartySerializer,
    SimpleProfileSerializer,
    PartySerializer,
    AllPostSerializer,
    AddressSerializer,
    CommitteeSerializer,
    HistoricalConstituencyCollectionSerializer,
    ContestedElectionCollectionSerializer,
    DeclaredInterestCollectionSerializer,
    ElectionSerializer,
    ExperienceCollectionSerializer,
    HistoricalPartyCollectionSerializer,
    FullProfileSerializer,
)
from api.serializers.maiden_speeches import MaidenSpeechCollectionSerializer
from api.serializers.subjects_of_interest import SubjectOfInterestCollectionSerializer
from api.views.decorators import api_key_required
from repository.models import (
    Constituency,
    Party,
    Person,
)

log = logging.getLogger(__name__)


class KeyRequiredViewSet(viewsets.ReadOnlyModelViewSet):
    """Base class for any ViewSet that requires a key/authorised user."""
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
            return SimpleProfileSerializer
        else:
            return InlineMemberSerializer


class BaseMemberViewSet(KeyRequiredViewSet):
    queryset = Person.objects.all()


class AddressViewSet(BaseMemberViewSet):
    """Physical and web addresses for a Person."""
    serializer_class = AddressSerializer


class CommitteeViewSet(BaseMemberViewSet):
    """Committee membership for a Person."""
    serializer_class = CommitteeSerializer


class ContestedElectionViewSet(BaseMemberViewSet):
    """Elections in which the Person ran but did not win."""
    serializer_class = ContestedElectionCollectionSerializer


class DeclaredInterestViewSet(BaseMemberViewSet):
    """Declared interests for a Person."""
    serializer_class = DeclaredInterestCollectionSerializer


class ElectionViewSet(BaseMemberViewSet):
    serializer_class = ElectionSerializer


class ExperienceViewSet(BaseMemberViewSet):
    """Experience entries for a Person."""
    serializer_class = ExperienceCollectionSerializer


class HistoricalConstituencyViewSet(BaseMemberViewSet):
    """Historical constituencies for a Person."""
    serializer_class = HistoricalConstituencyCollectionSerializer


class HistoricalPartyViewSet(BaseMemberViewSet):
    """Historical party associations for a Person."""
    serializer_class = HistoricalPartyCollectionSerializer


class MaidenSpeechViewSet(BaseMemberViewSet):
    """Maiden speeches for a Person."""
    serializer_class = MaidenSpeechCollectionSerializer


class PostViewSet(BaseMemberViewSet):
    """Governmental, Parliamentary, Opposition posts for a Person."""
    serializer_class = AllPostSerializer


class ProfileViewSet(BaseMemberViewSet):
    """Return all data about a person."""
    serializer_class = FullProfileSerializer


class SubjectOfInterestViewSet(BaseMemberViewSet):
    """Return a Person's subjects of interest."""
    serializer_class = SubjectOfInterestCollectionSerializer
