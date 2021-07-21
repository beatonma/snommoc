from rest_framework import serializers

from api.serializers.base import ReadOnlySerializer, DetailedModelSerializer
from api.serializers.bills import InlineBillSerializer
from api.serializers.inline import InlineMemberSerializer
from api.serializers.divisions.votes import GenericInlineDivisionSerializer
from surface.models import MessageOfTheDay


class MessageOfTheDaySerializer(DetailedModelSerializer):
    class Meta:
        model = MessageOfTheDay
        fields = [
            "title",
            "description",
            "action_url",
        ]


class _ZeitgeistPeopleSerializer(ReadOnlySerializer):
    reason = serializers.CharField()
    target = InlineMemberSerializer()


class _ZeitgeistBillsSerializer(ReadOnlySerializer):
    reason = serializers.CharField()
    target = InlineBillSerializer()


class _ZeitgeistDivisionsSerializer(ReadOnlySerializer):
    reason = serializers.CharField()
    target = GenericInlineDivisionSerializer()


class ZeitgeistSerializer(ReadOnlySerializer):
    motd = MessageOfTheDaySerializer(many=True)
    people = _ZeitgeistPeopleSerializer(many=True)
    divisions = _ZeitgeistDivisionsSerializer(many=True)
    bills = _ZeitgeistBillsSerializer(many=True)
