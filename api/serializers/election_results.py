"""

"""

import logging

from rest_framework import serializers

from api.serializers import (
    DetailedModelSerializer,
    InlineModelSerializer,
)
from repository.models import (
    ConstituencyCandidate,
    ConstituencyResultDetail,
)

log = logging.getLogger(__name__)


class ConstituencyCandidateSerializer(InlineModelSerializer):
    party_name = serializers.CharField(source='party')

    class Meta:
        model = ConstituencyCandidate
        fields = [
            'name',
            'party_name',
            'order',
            'votes',
        ]


class ConstituencyResultDetailsSerializer(DetailedModelSerializer):
    candidates = ConstituencyCandidateSerializer(many=True)

    class Meta:
        model = ConstituencyResultDetail
        fields = [
            'parliamentdotuk',
            'electorate',
            'turnout',
            'turnout_fraction',
            'result',
            'majority',
            'candidates',
        ]
