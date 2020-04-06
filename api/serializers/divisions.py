"""

"""

import logging

from rest_framework import serializers

from api.serializers import DetailedModelSerializer
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

    class Meta:
        model = CommonsDivisionVote
        fields = [
            'parliamentdotuk',
            'name',
            'vote',
        ]


class CommonsDivisionSerializer(DetailedModelSerializer):
    votes = CommonsDivisionVoteSerializer(many=True)

    class Meta:
        model = CommonsDivision
        fields = [
            'parliamentdotuk',
            'title',
            'date',
            'passed',
            'ayes',
            'noes',
            'votes',
        ]


class LordsDivisionVoteSerializer(DetailedModelSerializer):
    parliamentdotuk = serializers.IntegerField(source='person.parliamentdotuk')
    name = serializers.CharField(source='person.name')
    vote = serializers.CharField(source='vote_type')

    class Meta:
        model = LordsDivisionVote
        fields = [
            'parliamentdotuk',
            'name',
            'vote',
        ]


class LordsDivisionSerializer(DetailedModelSerializer):
    votes = LordsDivisionVoteSerializer(many=True)

    class Meta:
        model = LordsDivision
        fields = [
            'parliamentdotuk',
            'title',
            'description',
            'date',
            'passed',
            'ayes',
            'noes',
            'votes',
        ]


# class CommonsDivisionSerializer(DetailedSerializer):
#     class Meta:
#         model = CommonsDivision
#         fields = [
#             'parliamentdotuk',
#             'title',
#             'date',
#             'passed',
#         ]
#
#
# class CommonsVotesSerializer(DetailedSerializer):
#     division = CommonsDivisionSerializer()
#
#     class Meta:
#         model = CommonsDivisionVote
#         fields = [
#             'division',
#             'vote_type',
#         ]
#
#
# class LordsDivisionSerializer(DetailedSerializer):
#     class Meta:
#         model = LordsDivision
#         fields = [
#             'parliamentdotuk',
#             'title',
#             'date',
#             'passed',
#         ]
#
#
# class LordsVotesSerializer(DetailedSerializer):
#     division = LordsDivisionSerializer()
#
#     class Meta:
#         model = LordsDivisionVote
#         fields = [
#             'division',
#             'vote_type',
#         ]


# class VotesCollectionSerializer(DetailedSerializer):
#     commons = CommonsVotesSerializer(many=True, source='commonsdivisionvote_set')
#     lords = LordsVotesSerializer(many=True, source='lordsdivisionvote_set')
#
#     class Meta:
#         model = CommonsDivisionVote
#         fields = [
#             'commons',
#             'lords'
#         ]
