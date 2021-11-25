from rest_framework import serializers

from api import contract
from api.serializers.base import DetailedModelSerializer
from api.serializers.member import SimpleProfileSerializer
from api.serializers.parties import InlinePartySerializer
from repository.models import LordsDivision, LordsDivisionVote


class _LordsDivisionVoteSerializer(DetailedModelSerializer):
    parliamentdotuk = serializers.IntegerField(source="person.parliamentdotuk")
    name = serializers.CharField(source="person.name")
    vote = serializers.CharField(source="vote_type.name")
    party = InlinePartySerializer(source="person.party")

    class Meta:
        model = LordsDivisionVote
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.NAME,
            contract.DIVISION_VOTE,
            contract.PARTY,
        ]


class LordsDivisionSerializer(DetailedModelSerializer):
    description = serializers.CharField(source="amendment_motion_notes")
    house = serializers.ReadOnlyField(default=contract.HOUSE_LORDS)
    votes = _LordsDivisionVoteSerializer(many=True, source="votes_redux")
    whipped_vote = serializers.BooleanField(source="is_whipped")
    sponsor = SimpleProfileSerializer(source="sponsoring_member")

    class Meta:
        model = LordsDivision
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.TITLE,
            contract.DATE,
            contract.DESCRIPTION,
            contract.HOUSE,
            contract.DIVISION_SPONSOR,
            contract.DIVISION_PASSED,
            contract.DIVISION_VOTE_WHIPPED,
            contract.DIVISION_VOTE_AYES,
            contract.DIVISION_VOTE_NOES,
            contract.DIVISION_VOTES,
        ]
