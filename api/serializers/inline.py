"""

"""

import logging

from rest_framework import serializers

from api.serializers import InlineSerializer
from repository.models import (
    Constituency,
    Person,
    Party,
)
from api import endpoints
from repository.models.geography import Town

log = logging.getLogger(__name__)


class InlineConstituencySerializer(InlineSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name=f'{endpoints.CONSTITUENCY}-detail',
        read_only=True
    )

    class Meta:
        model = Constituency
        fields = [
            'name',
            'detail_url',
        ]


class InlineTownSerializer(InlineSerializer):
    town = serializers.CharField(source='name')
    country = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Town
        fields = [
            'town',
            'country',
        ]


class InlinePartySerializer(InlineSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name=f'{endpoints.PARTY}-detail',
        read_only=True
    )

    class Meta:
        model = Party
        fields = [
            'name',
            'detail_url',
        ]


class InlineMemberSerializer(InlineSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name=f'{endpoints.MEMBER}-detail',
        read_only=True
    )
    party = InlinePartySerializer()
    constituency = InlineConstituencySerializer()

    class Meta:
        model = Person
        fields = [
            'name',
            'detail_url',
            'party',
            'constituency',
        ]
