from rest_framework import serializers

from api import contract
from api.serializers.base import InlineModelSerializer
from repository.models import (
    CommonsDivision,
    CommonsDivisionVote,
    LordsDivision,
)


class GenericInlineDivisionSerializer(serializers.Serializer):
    parliamentdotuk = serializers.IntegerField()
    title = serializers.CharField()
    date = serializers.DateField()
    passed = serializers.BooleanField()
    house = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class _BaseInlineDivisionSerializer(InlineModelSerializer):
    _fields = [
        contract.PARLIAMENTDOTUK,
        contract.TITLE,
        contract.DATE,
        contract.DIVISION_PASSED,
    ]


class _InlineCommonsDivisionSerializer(_BaseInlineDivisionSerializer):
    class Meta:
        model = CommonsDivision
        fields = _BaseInlineDivisionSerializer._fields


class _InlineLordsDivisionSerializer(_BaseInlineDivisionSerializer):
    class Meta:
        model = LordsDivision
        fields = _BaseInlineDivisionSerializer._fields


class _BaseVoteSerializer(InlineModelSerializer):
    _fields = [
        contract.DIVISION,
        contract.DIVISION_VOTE_TYPE,
    ]


class CommonsVotesSerializer(_BaseVoteSerializer):
    division = _InlineCommonsDivisionSerializer()

    class Meta:
        model = CommonsDivisionVote
        fields = _BaseVoteSerializer._fields


class LordsVotesSerializer(_BaseVoteSerializer):
    division = _InlineLordsDivisionSerializer()

    class Meta:
        model = CommonsDivisionVote
        fields = _BaseVoteSerializer._fields
