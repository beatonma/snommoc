from rest_framework import serializers

from api import contract
from api.serializers.base import (
    DetailedModelSerializer,
    InlineModelSerializer,
)
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
    party_name = serializers.CharField(source="party")

    class Meta:
        model = ConstituencyCandidate
        fields = [
            contract.NAME,
            contract.ELECTION_CANDIDATE_PARTY_NAME,
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
