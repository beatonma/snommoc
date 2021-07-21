from rest_framework import serializers

from api import contract
from api.serializers.base import DetailedModelSerializer
from repository.models import CommitteeMember
from repository.models.committees import CommitteeChair


class _CommitteeChairSerializer(DetailedModelSerializer):
    class Meta:
        model = CommitteeChair
        fields = [
            contract.START,
            contract.END,
        ]


class CommitteeMemberSerializer(DetailedModelSerializer):
    parliamentdotuk = serializers.IntegerField(source="committee.parliamentdotuk")
    name = serializers.CharField(source="committee.name")
    chair = _CommitteeChairSerializer(many=True, source="committeechair_set")

    class Meta:
        model = CommitteeMember
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.NAME,
            contract.START,
            contract.END,
            contract.COMMITTEE_CHAIR,
        ]
