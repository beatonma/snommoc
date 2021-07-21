from rest_framework import serializers

from api.serializers.base import (
    DetailedModelSerializer,
)
from repository.models import (
    CommonsDivision,
    CommonsDivisionVote,
    LordsDivisionVote,
    LordsDivision,
)
from api.serializers.parties import InlinePartySerializer


class _BaseVotesSerializer(DetailedModelSerializer):
    parliamentdotuk = serializers.IntegerField(source="person.parliamentdotuk")
    name = serializers.CharField(source="person.name")
    vote = serializers.CharField(source="vote_type")
    party = InlinePartySerializer(source="person.party")

    _fields = [
        "parliamentdotuk",
        "name",
        "vote",
        "party",
    ]


class _CommonsDivisionVoteSerializer(_BaseVotesSerializer):
    class Meta:
        model = CommonsDivisionVote
        fields = _BaseVotesSerializer._fields


class _LordsDivisionVoteSerializer(_BaseVotesSerializer):
    class Meta:
        model = LordsDivisionVote
        fields = _BaseVotesSerializer._fields


class CommonsDivisionSerializer(DetailedModelSerializer):
    house = serializers.CharField()
    votes = _CommonsDivisionVoteSerializer(many=True)

    class Meta:
        model = CommonsDivision
        fields = [
            "parliamentdotuk",
            "title",
            "date",
            "house",
            "passed",
            "ayes",
            "noes",
            "did_not_vote",
            "abstentions",
            "deferred_vote",
            "errors",
            "non_eligible",
            "suspended_or_expelled",
            "votes",
        ]


class LordsDivisionSerializer(DetailedModelSerializer):
    house = serializers.CharField()
    votes = _LordsDivisionVoteSerializer(many=True)

    class Meta:
        model = LordsDivision
        fields = [
            "parliamentdotuk",
            "title",
            "description",
            "date",
            "house",
            "passed",
            "ayes",
            "noes",
            "whipped_vote",
            "votes",
        ]
