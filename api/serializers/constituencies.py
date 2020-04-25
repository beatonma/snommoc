"""

"""

import logging

from rest_framework import serializers

from api.serializers import (
    DetailedModelSerializer,
    InlineMemberSerializer,
    InlineModelSerializer,
)
from api.serializers.election import ElectionSerializer
from repository.models import (
    Constituency,
    ConstituencyBoundary,
    ConstituencyResult,
    Person,
)

log = logging.getLogger(__name__)


class MinimalConstituencySerializer(InlineModelSerializer):
    class Meta:
        model = Constituency
        fields = [
            'parliamentdotuk',
            'name',
        ]


class ConstituencyBoundarySerializer(DetailedModelSerializer):
    kml = serializers.CharField(source='boundary_kml')

    class Meta:
        model = ConstituencyBoundary
        fields = [
            'kml',
            'center_latitude',
            'center_longitude',
            'area',
            'boundary_length',
        ]


class ConstituencySerializer(DetailedModelSerializer):
    mp = InlineMemberSerializer()
    boundary = ConstituencyBoundarySerializer(source='constituencyboundary')

    class Meta:
        model = Constituency
        fields = [
            'parliamentdotuk',
            'name',
            'mp',
            'start',
            'end',
            'boundary',
        ]


class HistoricalConstituencySerializer(DetailedModelSerializer):
    constituency = MinimalConstituencySerializer()
    election = ElectionSerializer()

    class Meta:
        model = ConstituencyResult
        fields = [
            'constituency',
            'start',
            'end',
            'election',
        ]


class HistoricalConstituencyCollectionSerializer(DetailedModelSerializer):
    constituencies = HistoricalConstituencySerializer(many=True, source='constituencyresult_set')

    class Meta:
        model = Person
        fields = [
            'constituencies',
        ]
