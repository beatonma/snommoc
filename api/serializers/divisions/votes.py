from rest_framework import serializers

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


class _InlineCommonsDivisionSerializer(InlineModelSerializer):
    class Meta:
        model = CommonsDivision
        fields = [
            "parliamentdotuk",
            "title",
            "date",
            "passed",
        ]


class _InlineLordsDivisionSerializer(InlineModelSerializer):
    class Meta:
        model = LordsDivision
        fields = [
            "parliamentdotuk",
            "title",
            "date",
            "passed",
        ]


class CommonsVotesSerializer(InlineModelSerializer):
    division = _InlineCommonsDivisionSerializer()

    class Meta:
        model = CommonsDivisionVote
        fields = [
            "division",
            "vote_type",
        ]


class LordsVotesSerializer(InlineModelSerializer):
    division = _InlineLordsDivisionSerializer()

    class Meta:
        model = CommonsDivisionVote
        fields = [
            "division",
            "vote_type",
        ]
