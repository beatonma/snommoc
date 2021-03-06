"""

"""

import logging

from rest_framework import serializers

from api.serializers import (
    DetailedModelSerializer,
    InlinePartySerializer,
)
from repository.models import (
    Bill,
    BillSponsor,
    BillPublication,
    BillType,
    BillStage,
    ParliamentarySession,
    BillStageSitting,
)

log = logging.getLogger(__name__)


class BillSponsorSerializer(DetailedModelSerializer):
    parliamentdotuk = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    party = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.name if obj.person is None else obj.person.name

    def get_parliamentdotuk(self, obj):
        return None if obj.person is None else obj.person.parliamentdotuk

    def get_party(self, obj):
        return None if obj.person is None else InlinePartySerializer(obj.person.party).data

    class Meta:
        model = BillSponsor
        fields = [
            'parliamentdotuk',
            'name',
            'party',
        ]


class BillPublicationSerializer(DetailedModelSerializer):
    class Meta:
        model = BillPublication
        fields = [
            'parliamentdotuk',
            'title',
        ]


class BillTypeSerializer(DetailedModelSerializer):
    class Meta:
        model = BillType
        fields = [
            'name',
            'description',
        ]


class BillStageSittingSerializer(DetailedModelSerializer):
    class Meta:
        model = BillStageSitting
        fields = [
            'parliamentdotuk',
            'date',
            'formal',
            'provisional',
        ]


class BillStageSerializer(DetailedModelSerializer):
    type = serializers.CharField(source='bill_stage_type.name')
    sittings = BillStageSittingSerializer(many=True)

    class Meta:
        model = BillStage
        fields = [
            'parliamentdotuk',
            'sittings',
            'type',
        ]


class SessionSerializer(DetailedModelSerializer):
    class Meta:
        model = ParliamentarySession
        fields = [
            'parliamentdotuk',
            'name',
        ]


class BillSerializer(DetailedModelSerializer):
    sponsors = BillSponsorSerializer(many=True, source='billsponsor_set')
    publications = BillPublicationSerializer(many=True, source='billpublication_set')
    type = BillTypeSerializer(source='bill_type')
    session = SessionSerializer()
    stages = BillStageSerializer(many=True, source='billstage_set')

    class Meta:
        model = Bill
        fields = [
            'parliamentdotuk',
            'title',
            'description',
            'act_name',
            'label',
            'homepage',
            'date',
            'ballot_number',
            'bill_chapter',
            'is_private',
            'is_money_bill',
            'public_involvement_allowed',
            'publications',
            'session',
            'sponsors',
            'stages',
            'type',
        ]
