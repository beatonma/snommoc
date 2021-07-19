import logging

from rest_framework import serializers

from api.serializers.base import ReadOnlySerializer
from api.serializers.bills import InlineBillSerializer
from api.serializers.inline import InlineMemberSerializer
from api.serializers.motd import MessageOfTheDaySerializer
from api.serializers.votes import GenericInlineDivisionSerializer

log = logging.getLogger(__name__)


class ZeitgeistPeopleSerializer(ReadOnlySerializer):
    reason = serializers.CharField()
    target = InlineMemberSerializer()


class ZeitgeistBillsSerializer(ReadOnlySerializer):
    reason = serializers.CharField()
    target = InlineBillSerializer()


class ZeitgeistDivisionsSerializer(ReadOnlySerializer):
    reason = serializers.CharField()
    target = GenericInlineDivisionSerializer()


class ZeitgeistSerializer(ReadOnlySerializer):
    motd = MessageOfTheDaySerializer(many=True)
    people = ZeitgeistPeopleSerializer(many=True)
    divisions = ZeitgeistDivisionsSerializer(many=True)
    bills = ZeitgeistBillsSerializer(many=True)
