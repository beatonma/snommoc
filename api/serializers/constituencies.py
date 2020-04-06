"""

"""

import logging

from api.serializers import (
    DetailedModelSerializer,
    InlineMemberSerializer,
    InlineModelSerializer,
)
from api.serializers.election import ElectionSerializer
from repository.models import (
    Constituency,
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


class ConstituencySerializer(DetailedModelSerializer):
    mp = InlineMemberSerializer()

    class Meta:
        model = Constituency
        fields = [
            'parliamentdotuk',
            'name',
            'mp',
            'start',
            'end',
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
