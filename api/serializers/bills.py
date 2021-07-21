from rest_framework import serializers

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
            "parliamentdotuk",
            "title",
            "description",
            "date",
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
            "parliamentdotuk",
            "name",
            "party",
        ]


class _BillPublicationSerializer(DetailedModelSerializer):
    class Meta:
        model = BillPublication
        fields = [
            "parliamentdotuk",
            "title",
        ]


class _BillTypeSerializer(DetailedModelSerializer):
    class Meta:
        model = BillType
        fields = [
            "name",
            "description",
        ]


class _BillStageSittingSerializer(DetailedModelSerializer):
    class Meta:
        model = BillStageSitting
        fields = [
            "parliamentdotuk",
            "date",
            "formal",
            "provisional",
        ]


class _BillStageSerializer(DetailedModelSerializer):
    type = serializers.CharField(source="bill_stage_type.name")
    sittings = _BillStageSittingSerializer(many=True)

    class Meta:
        model = BillStage
        fields = [
            "parliamentdotuk",
            "sittings",
            "type",
        ]


class _SessionSerializer(DetailedModelSerializer):
    class Meta:
        model = ParliamentarySession
        fields = [
            "parliamentdotuk",
            "name",
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
            "parliamentdotuk",
            "title",
            "description",
            "act_name",
            "label",
            "homepage",
            "date",
            "ballot_number",
            "bill_chapter",
            "is_private",
            "is_money_bill",
            "public_involvement_allowed",
            "publications",
            "session",
            "sponsors",
            "stages",
            "type",
        ]
