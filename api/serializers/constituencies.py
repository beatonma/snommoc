"""

"""

import logging

from api.serializers import (
    DetailedSerializer,
    InlineMemberSerializer,
    InlineSerializer,
)
from api.serializers.election import ElectionSerializer
from repository.models import (
    Constituency,
    ConstituencyResult,
    Person,
)

log = logging.getLogger(__name__)


class MinimalConstituencySerializer(InlineSerializer):
    class Meta:
        model = Constituency
        fields = [
            'parliamentdotuk',
            'name',
        ]


class ConstituencySerializer(DetailedSerializer):
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


class HistoricalConstituencySerializer(DetailedSerializer):
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


class HistoricalConstituencyCollectionSerializer(DetailedSerializer):
    constituencies = HistoricalConstituencySerializer(many=True, source='constituencyresult_set')

    class Meta:
        model = Person
        fields = [
            'constituencies',
        ]
