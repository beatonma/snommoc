from rest_framework import serializers

from api import contract
from api.serializers.base import ReadOnlySerializer, DetailedModelSerializer
from api.serializers.bills import InlineBillSerializer
from api.serializers.inline import InlineMemberSerializer
from api.serializers.divisions.votes import GenericInlineDivisionSerializer
from surface.models import MessageOfTheDay


class MessageOfTheDaySerializer(DetailedModelSerializer):
    class Meta:
        model = MessageOfTheDay
        fields = [
            contract.TITLE,
            contract.DESCRIPTION,
            contract.MOTD_ACTION_URL,
        ]


class _ZeitgeistPeopleSerializer(ReadOnlySerializer):
    priority = serializers.IntegerField()
    reason = serializers.CharField()
    target = InlineMemberSerializer()


class _ZeitgeistBillsSerializer(ReadOnlySerializer):
    priority = serializers.IntegerField()
    reason = serializers.CharField()
    target = InlineBillSerializer()


class _ZeitgeistDivisionsSerializer(ReadOnlySerializer):
    priority = serializers.IntegerField()
    reason = serializers.CharField()
    target = GenericInlineDivisionSerializer()


class ZeitgeistSerializer(ReadOnlySerializer):
    motd = MessageOfTheDaySerializer(many=True)
    people = _ZeitgeistPeopleSerializer(many=True)
    divisions = _ZeitgeistDivisionsSerializer(many=True)
    bills = _ZeitgeistBillsSerializer(many=True)
