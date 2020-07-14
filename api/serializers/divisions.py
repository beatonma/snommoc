"""

"""

import logging

from rest_framework import serializers

from api.serializers import (
    DetailedModelSerializer,
    InlinePartySerializer,
)
from repository.models import (
    CommonsDivision,
    CommonsDivisionVote,
    LordsDivisionVote,
    LordsDivision,
)

log = logging.getLogger(__name__)


class CommonsDivisionVoteSerializer(DetailedModelSerializer):
    parliamentdotuk = serializers.IntegerField(source='person.parliamentdotuk')
    name = serializers.CharField(source='person.name')
    vote = serializers.CharField(source='vote_type')
    party = InlinePartySerializer(source='person.party')

    class Meta:
        model = CommonsDivisionVote
        fields = [
            'parliamentdotuk',
            'name',
            'vote',
            'party',
        ]


class CommonsDivisionSerializer(DetailedModelSerializer):
    house = serializers.CharField()
    votes = CommonsDivisionVoteSerializer(many=True)

    class Meta:
        model = CommonsDivision
        fields = [
            'parliamentdotuk',
            'title',
            'date',
            'house',
            'passed',
            'ayes',
            'noes',
            'did_not_vote',
            'abstentions',
            'deferred_vote',
            'errors',
            'non_eligible',
            'suspended_or_expelled',
            'votes',
        ]


class LordsDivisionVoteSerializer(DetailedModelSerializer):
    parliamentdotuk = serializers.IntegerField(source='person.parliamentdotuk')
    name = serializers.CharField(source='person.name')
    vote = serializers.CharField(source='vote_type')
    party = InlinePartySerializer(source='person.party')

    class Meta:
        model = LordsDivisionVote
        fields = [
            'parliamentdotuk',
            'name',
            'vote',
            'party',
        ]


class LordsDivisionSerializer(DetailedModelSerializer):
    house = serializers.CharField()
    votes = LordsDivisionVoteSerializer(many=True)

    class Meta:
        model = LordsDivision
        fields = [
            'parliamentdotuk',
            'title',
            'description',
            'date',
            'house',
            'passed',
            'ayes',
            'noes',
            'whipped_vote',
            'votes',
        ]
