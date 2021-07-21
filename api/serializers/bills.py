from rest_framework import serializers

from api import contract
from api.serializers.base import DetailedModelSerializer, InlineModelSerializer
from api.serializers.inline import InlinePartySerializer
from repository.models import (
    Bill,
    BillSponsor,
    BillPublication,
    BillType,
    BillStage,
    ParliamentarySession,
    BillStageSitting,
)


class InlineBillSerializer(InlineModelSerializer):
    class Meta:
        model = Bill
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.TITLE,
            contract.DESCRIPTION,
            contract.DATE,
        ]


class _BillSponsorSerializer(DetailedModelSerializer):
    parliamentdotuk = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    party = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.name if obj.person is None else obj.person.name

    def get_parliamentdotuk(self, obj):
        return None if obj.person is None else obj.person.parliamentdotuk

    def get_party(self, obj):
        return (
            None if obj.person is None else InlinePartySerializer(obj.person.party).data
        )

    class Meta:
        model = BillSponsor
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.NAME,
            contract.PARTY,
        ]


class _BillPublicationSerializer(DetailedModelSerializer):
    class Meta:
        model = BillPublication
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.TITLE,
        ]


class _BillTypeSerializer(DetailedModelSerializer):
    class Meta:
        model = BillType
        fields = [
            contract.NAME,
            contract.DESCRIPTION,
        ]


class _BillStageSittingSerializer(DetailedModelSerializer):
    class Meta:
        model = BillStageSitting
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.DATE,
            contract.BILL_SITTING_FORMAL,
            contract.BILL_SITTING_PROVISIONAL,
        ]


class _BillStageSerializer(DetailedModelSerializer):
    type = serializers.CharField(source="bill_stage_type.name")
    sittings = _BillStageSittingSerializer(many=True)

    class Meta:
        model = BillStage
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.BILL_SITTINGS,
            contract.BILL_TYPE,
        ]


class _SessionSerializer(DetailedModelSerializer):
    class Meta:
        model = ParliamentarySession
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.NAME,
        ]


class BillSerializer(DetailedModelSerializer):
    sponsors = _BillSponsorSerializer(many=True, source="billsponsor_set")
    publications = _BillPublicationSerializer(many=True, source="billpublication_set")
    type = _BillTypeSerializer(source="bill_type")
    session = _SessionSerializer()
    stages = _BillStageSerializer(many=True, source="billstage_set")

    class Meta:
        model = Bill
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.DATE,
            contract.TITLE,
            contract.DESCRIPTION,
            contract.BILL_ACT_NAME,
            contract.BILL_LABEL,
            contract.BILL_HOMEPAGE,
            contract.BILL_BALLOT_NUMBER,
            contract.BILL_CHAPTER,
            contract.BILL_IS_PRIVATE,
            contract.BILL_IS_MONEY_BILL,
            contract.BILL_PUBLIC_INVOLVEMENT_ALLOWED,
            contract.BILL_PUBLICATIONS,
            contract.SESSION,
            contract.BILL_SPONSORS,
            contract.BILL_STAGES,
            contract.BILL_TYPE,
        ]
