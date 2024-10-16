from rest_framework import serializers

from api import contract
from api.serializers.base import DetailedModelSerializer
from api.serializers.parties import InlinePartySerializer
from repository.models import (
    CommonsDivision,
    CommonsDivisionVote,
)


class _CommonsDivisionVoteSerializer(DetailedModelSerializer):
    parliamentdotuk = serializers.IntegerField(source="person.parliamentdotuk")
    name = serializers.CharField(source="person.name")
    vote = serializers.CharField(source="vote_type")
    party = InlinePartySerializer(source="person.party")

    class Meta:
        model = CommonsDivisionVote
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.NAME,
            contract.DIVISION_VOTE,
            contract.PARTY,
        ]


class CommonsDivisionSerializer(DetailedModelSerializer):
    house = serializers.CharField()
    votes = _CommonsDivisionVoteSerializer(many=True)

    class Meta:
        model = CommonsDivision
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.TITLE,
            contract.DATE,
            contract.HOUSE,
            contract.DIVISION_PASSED,
            contract.DIVISION_VOTE_AYES,
            contract.DIVISION_VOTE_NOES,
            contract.DIVISION_VOTES,
            contract.DIVISION_VOTE_DID_NOT_VOTE,
            contract.DIVISION_VOTE_ABSTENTIONS,
            contract.DIVISION_VOTE_DEFERRED,
            contract.DIVISION_VOTE_ERRORS,
            contract.DIVISION_VOTE_NON_ELIGIBLE,
            contract.DIVISION_VOTE_SUSPENDED_EXPELLED,
        ]
