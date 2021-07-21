from rest_framework import serializers

from api import contract
from api.serializers.base import DetailedModelSerializer
from api.serializers.parties import InlinePartySerializer
from repository.models import (
    CommonsDivision,
    CommonsDivisionVote,
    LordsDivision,
    LordsDivisionVote,
)


class _BaseVotesSerializer(DetailedModelSerializer):
    parliamentdotuk = serializers.IntegerField(source="person.parliamentdotuk")
    name = serializers.CharField(source="person.name")
    vote = serializers.CharField(source="vote_type")
    party = InlinePartySerializer(source="person.party")

    _fields = [
        contract.PARLIAMENTDOTUK,
        contract.NAME,
        contract.DIVISION_VOTE,
        contract.PARTY,
    ]


class _CommonsDivisionVoteSerializer(_BaseVotesSerializer):
    class Meta:
        model = CommonsDivisionVote
        fields = _BaseVotesSerializer._fields


class _LordsDivisionVoteSerializer(_BaseVotesSerializer):
    class Meta:
        model = LordsDivisionVote
        fields = _BaseVotesSerializer._fields


class _BaseDivisionSerializer(DetailedModelSerializer):
    house = serializers.CharField()

    _fields = [
        contract.PARLIAMENTDOTUK,
        contract.TITLE,
        contract.DATE,
        contract.HOUSE,
        contract.DIVISION_PASSED,
        contract.DIVISION_VOTE_AYES,
        contract.DIVISION_VOTE_NOES,
        contract.DIVISION_VOTES,
    ]


class CommonsDivisionSerializer(_BaseDivisionSerializer):
    votes = _CommonsDivisionVoteSerializer(many=True)

    class Meta:
        model = CommonsDivision
        fields = _BaseDivisionSerializer._fields + [
            contract.DIVISION_VOTE_DID_NOT_VOTE,
            contract.DIVISION_VOTE_ABSTENTIONS,
            contract.DIVISION_VOTE_DEFERRED,
            contract.DIVISION_VOTE_ERRORS,
            contract.DIVISION_VOTE_NON_ELIGIBLE,
            contract.DIVISION_VOTE_SUSPENDED_EXPELLED,
        ]


class LordsDivisionSerializer(_BaseDivisionSerializer):
    votes = _LordsDivisionVoteSerializer(many=True)

    class Meta:
        model = LordsDivision
        fields = _BaseDivisionSerializer._fields + [
            contract.DESCRIPTION,
            contract.DIVISION_VOTE_WHIPPED,
        ]
