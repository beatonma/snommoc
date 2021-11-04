from rest_framework import serializers

from api import contract
from api.serializers.base import (
    DetailedModelSerializer,
    InlineModelSerializer,
)
from api.serializers.member import SimpleProfileSerializer
from api.serializers.parties import InlinePartySerializer
from repository.models import (
    ConstituencyCandidate,
    ConstituencyResult,
    ConstituencyResultDetail,
)
from api.serializers.inline import InlineConstituencySerializer, InlineMemberSerializer
from api.serializers.election import ElectionSerializer


class ElectionResultSerializer(DetailedModelSerializer):
    election = ElectionSerializer()
    mp = InlineMemberSerializer()

    class Meta:
        model = ConstituencyResult
        fields = [
            contract.ELECTION,
            contract.MP,
        ]


class _ConstituencyCandidateSerializer(InlineModelSerializer):
    party_name = serializers.CharField()
    party = InlinePartySerializer()
    profile = serializers.SerializerMethodField()

    def get_profile(self, obj):
        return None if obj.person is None else SimpleProfileSerializer(obj.person).data

    class Meta:
        model = ConstituencyCandidate
        fields = [
            contract.NAME,
            contract.PROFILE,
            contract.ELECTION_CANDIDATE_PARTY_NAME,
            contract.PARTY,
            contract.ELECTION_CANDIDATE_ORDER,
            contract.ELECTION_CANDIDATE_VOTES,
        ]


class ConstituencyResultDetailsSerializer(DetailedModelSerializer):
    candidates = _ConstituencyCandidateSerializer(many=True)
    constituency = InlineConstituencySerializer(
        source="constituency_result.constituency"
    )
    election = ElectionSerializer(source="constituency_result.election")

    class Meta:
        model = ConstituencyResultDetail
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.ELECTION_ELECTORATE,
            contract.ELECTION_TURNOUT,
            contract.ELECTION_TURNOUT_FRACTION,
            contract.ELECTION_RESULT,
            contract.ELECTION_MAJORITY,
            contract.CONSTITUENCY,
            contract.ELECTION,
            contract.ELECTION_CANDIDATES,
        ]
