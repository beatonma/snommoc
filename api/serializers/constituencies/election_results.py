from rest_framework import serializers

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
            "election",
            "mp",
        ]


class _ConstituencyCandidateSerializer(InlineModelSerializer):
    party_name = serializers.CharField(source="party")

    class Meta:
        model = ConstituencyCandidate
        fields = [
            "name",
            "party_name",
            "order",
            "votes",
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
            "parliamentdotuk",
            "electorate",
            "turnout",
            "turnout_fraction",
            "result",
            "majority",
            "constituency",
            "election",
            "candidates",
        ]
