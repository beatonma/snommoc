from rest_framework import serializers

from api import contract
from api.serializers.base import InlineModelSerializer
from api.serializers.parties import InlinePartySerializer
from repository.models import (
    Constituency,
    Person,
)


class InlineConstituencySerializer(InlineModelSerializer):
    class Meta:
        model = Constituency
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.NAME,
        ]


class InlineMemberSerializer(InlineModelSerializer):
    party = InlinePartySerializer()
    constituency = InlineConstituencySerializer()
    portrait = serializers.URLField(source="memberportrait.square_url")

    class Meta:
        model = Person
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.MEMBER_NAME,
            contract.PORTRAIT,
            contract.PARTY,
            contract.CONSTITUENCY,
            contract.CURRENT_POST,
        ]
