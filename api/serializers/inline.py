import logging

from rest_framework import serializers

from api.serializers.base import InlineModelSerializer
from repository.models import (
    Constituency,
    Person,
)
from api.serializers.parties import InlinePartySerializer

log = logging.getLogger(__name__)


class InlineConstituencySerializer(InlineModelSerializer):
    class Meta:
        model = Constituency
        fields = [
            "parliamentdotuk",
            "name",
        ]


class InlineMemberSerializer(InlineModelSerializer):
    party = InlinePartySerializer()
    constituency = InlineConstituencySerializer()
    portrait = serializers.URLField(source="memberportrait.square_url")

    class Meta:
        model = Person
        fields = [
            "parliamentdotuk",
            "name",
            "portrait",
            "party",
            "constituency",
            "current_post",
        ]
