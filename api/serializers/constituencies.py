import logging

from rest_framework import serializers

from api.serializers.election import ElectionSerializer
from repository.models import (
    Constituency,
    ConstituencyBoundary,
    ConstituencyResult,
)
from api.serializers.base import DetailedModelSerializer, InlineModelSerializer
from api.serializers.inline import InlineMemberSerializer

log = logging.getLogger(__name__)


class MinimalConstituencySerializer(InlineModelSerializer):
    class Meta:
        model = Constituency
        fields = [
            "parliamentdotuk",
            "name",
        ]


class ElectionResultSerializer(DetailedModelSerializer):
    election = ElectionSerializer()
    mp = InlineMemberSerializer()

    class Meta:
        model = ConstituencyResult
        fields = [
            "election",
            "mp",
        ]


class ConstituencyBoundarySerializer(DetailedModelSerializer):
    kml = serializers.CharField(source="boundary_kml")

    class Meta:
        model = ConstituencyBoundary
        fields = [
            "kml",
            "center_latitude",
            "center_longitude",
            "area",
            "boundary_length",
        ]


class ConstituencySerializer(DetailedModelSerializer):
    mp = InlineMemberSerializer()
    boundary = ConstituencyBoundarySerializer(source="constituencyboundary")
    results = ElectionResultSerializer(source="constituencyresult_set", many=True)

    class Meta:
        model = Constituency
        fields = [
            "parliamentdotuk",
            "name",
            "mp",
            "start",
            "end",
            "boundary",
            "results",
        ]


class HistoricalConstituencySerializer(DetailedModelSerializer):
    constituency = MinimalConstituencySerializer()
    election = ElectionSerializer()

    class Meta:
        model = ConstituencyResult
        fields = [
            "constituency",
            "start",
            "end",
            "election",
        ]
