"""

"""

import logging

from rest_framework import serializers

from api.serializers import InlineModelSerializer
from repository.models import (
    Constituency,
    Person,
    Party,
    Bill,
)
from repository.models.geography import Town

log = logging.getLogger(__name__)


class InlineConstituencySerializer(InlineModelSerializer):
    class Meta:
        model = Constituency
        fields = [
            'parliamentdotuk',
            'name',
        ]


class InlineTownSerializer(InlineModelSerializer):
    town = serializers.CharField(source='name')
    country = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Town
        fields = [
            'town',
            'country',
        ]


class InlinePartySerializer(InlineModelSerializer):
    class Meta:
        model = Party
        fields = [
            'parliamentdotuk',
            'name',
        ]


class InlineMemberSerializer(InlineModelSerializer):
    party = InlinePartySerializer()
    constituency = InlineConstituencySerializer()
    portrait = serializers.URLField(source='memberportrait.square_url')

    class Meta:
        model = Person
        fields = [
            'parliamentdotuk',
            'name',
            'portrait',
            'party',
            'constituency',
            'current_post',
        ]


class InlineBillSerializer(InlineModelSerializer):
    class Meta:
        model = Bill
        fields = [
            'parliamentdotuk',
            'title',
            'description',
            'date',
        ]
