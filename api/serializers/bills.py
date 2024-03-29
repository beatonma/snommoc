from rest_framework import serializers

from api import contract
from api.serializers.base import DetailedModelSerializer, InlineModelSerializer
from api.serializers.member import SimpleProfileSerializer
from repository.models import Bill, Organisation, ParliamentarySession
from repository.models.bill import (
    BillPublication,
    BillPublicationLink,
    BillSponsor,
    BillStage,
    BillType,
)


class _SessionSerializer(DetailedModelSerializer):
    class Meta:
        model = ParliamentarySession
        fields = (
            contract.PARLIAMENTDOTUK,
            contract.NAME,
        )


class _OrganisationSerializer(DetailedModelSerializer):
    class Meta:
        model = Organisation
        fields = (
            contract.NAME,
            contract.URL,
        )


class InlineBillSerializer(InlineModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField(source="summary")

    class Meta:
        model = Bill
        fields = (
            contract.PARLIAMENTDOTUK,
            contract.TITLE,
            contract.DESCRIPTION,
            contract.BILL_LAST_UPDATE,
        )


class _BillSponsorSerializer(DetailedModelSerializer):
    id = serializers.IntegerField(source="pk")
    profile = SimpleProfileSerializer(source="member")
    organisation = _OrganisationSerializer()

    class Meta:
        model = BillSponsor
        fields = (
            contract.ID,
            contract.PROFILE,
            contract.ORGANISATION,
        )


class _BillPublicationLinkSerializer(DetailedModelSerializer):
    class Meta:
        model = BillPublicationLink
        fields = (
            "title",
            "url",
            "content_type",
        )


class _BillPublicationSerializer(DetailedModelSerializer):
    links = _BillPublicationLinkSerializer(many=True)
    date = serializers.SerializerMethodField()
    type = serializers.CharField(source="publication_type.name")

    def get_date(self, publication: BillPublication):
        return publication.display_date.date()

    class Meta:
        model = BillPublication
        fields = (
            contract.PARLIAMENTDOTUK,
            contract.TITLE,
            contract.DATE,
            contract.LINKS,
            contract.TYPE,
        )


class _BillTypeSerializer(DetailedModelSerializer):
    category = serializers.CharField(source="category.name")

    class Meta:
        model = BillType
        fields = (
            contract.PARLIAMENTDOTUK,
            contract.NAME,
            contract.DESCRIPTION,
            contract.CATEGORY,
        )


class _BillStageSerializer(DetailedModelSerializer):
    sittings = serializers.SerializerMethodField()
    session = _SessionSerializer()
    house = serializers.CharField(source="house.name")
    sitting_latest = serializers.SerializerMethodField()

    def get_sittings(self, stage: BillStage):
        sittings = stage.sittings.values_list("date", flat=True)
        return map(lambda x: x.date(), sittings)

    def get_sitting_latest(self, stage: BillStage):
        return stage.sittings.order_by("-date").first().date.date()

    class Meta:
        model = BillStage
        fields = (
            contract.PARLIAMENTDOTUK,
            contract.DESCRIPTION,
            contract.HOUSE,
            contract.SESSION,
            contract.BILL_SITTING_LATEST,
            contract.BILL_SITTINGS,
        )


class BillSerializer(DetailedModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField(source="summary")
    sponsors = _BillSponsorSerializer(many=True)
    publications = _BillPublicationSerializer(many=True)
    type = _BillTypeSerializer(source="bill_type")
    session_introduced = _SessionSerializer()
    sessions = _SessionSerializer(many=True)
    current_stage = _BillStageSerializer()
    stages = _BillStageSerializer(many=True)

    class Meta:
        model = Bill
        fields = (
            contract.PARLIAMENTDOTUK,
            contract.BILL_LAST_UPDATE,
            contract.TITLE,
            contract.DESCRIPTION,
            contract.BILL_IS_ACT,
            contract.BILL_IS_DEFEATED,
            contract.BILL_DATE_WITHDRAWN,
            contract.TYPE,
            contract.BILL_SESSION_INTRODUCED,
            contract.BILL_SESSIONS,
            contract.BILL_CURRENT_STAGE,
            contract.BILL_STAGES,
            contract.BILL_SPONSORS,
            contract.BILL_PUBLICATIONS,
        )
