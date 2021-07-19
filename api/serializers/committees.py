import logging

from rest_framework import serializers

from api.serializers.base import DetailedModelSerializer
from repository.models import (
    CommitteeMember,
    Person,
)
from repository.models.committees import CommitteeChair

log = logging.getLogger(__name__)


class CommitteeChairSerializer(DetailedModelSerializer):
    class Meta:
        model = CommitteeChair
        fields = [
            "start",
            "end",
        ]


class CommitteeMemberSerializer(DetailedModelSerializer):
    parliamentdotuk = serializers.IntegerField(source="committee.parliamentdotuk")
    name = serializers.CharField(source="committee.name")
    chair = CommitteeChairSerializer(many=True, source="committeechair_set")

    class Meta:
        model = CommitteeMember
        fields = [
            "parliamentdotuk",
            "name",
            "start",
            "end",
            "chair",
        ]


class CommitteeSerializer(DetailedModelSerializer):
    committees = CommitteeMemberSerializer(many=True, source="committeemember_set")

    class Meta:
        model = Person
        fields = [
            "committees",
        ]
