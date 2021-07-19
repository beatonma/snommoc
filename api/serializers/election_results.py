import logging

from rest_framework import serializers

from api.serializers.base import DetailedModelSerializer, InlineModelSerializer
from repository.models import (
    ConstituencyCandidate,
    ConstituencyResultDetail,
)
from api.serializers.inline import InlineConstituencySerializer
from api.serializers.election import ElectionSerializer

log = logging.getLogger(__name__)


class ConstituencyCandidateSerializer(InlineModelSerializer):
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
    candidates = ConstituencyCandidateSerializer(many=True)
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
