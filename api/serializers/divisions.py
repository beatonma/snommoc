"""

"""

import logging

from api.serializers import DetailedSerializer
from repository.models import (
    CommonsDivision,
    CommonsDivisionVote,
    LordsDivision,
    LordsDivisionVote,
)

log = logging.getLogger(__name__)


class CommonsDivisionSerializer(DetailedSerializer):
    class Meta:
        model = CommonsDivision
        fields = [
            'parliamentdotuk',
            'title',
            'date',
            'passed',
        ]


class CommonsVotesSerializer(DetailedSerializer):
    division = CommonsDivisionSerializer()

    class Meta:
        model = CommonsDivisionVote
        fields = [
            'division',
            'vote_type',
        ]


class LordsDivisionSerializer(DetailedSerializer):
    class Meta:
        model = LordsDivision
        fields = [
            'parliamentdotuk',
            'title',
            'date',
            'passed',
        ]


class LordsVotesSerializer(DetailedSerializer):
    division = LordsDivisionSerializer()

    class Meta:
        model = LordsDivisionVote
        fields = [
            'division',
            'vote_type',
        ]


class VotesCollectionSerializer(DetailedSerializer):
    commons = CommonsVotesSerializer(many=True, source='commonsdivisionvote_set')
    lords = LordsVotesSerializer(many=True, source='lordsdivisionvote_set')

    class Meta:
        model = CommonsDivisionVote
        fields = [
            'commons',
            'lords'
        ]
