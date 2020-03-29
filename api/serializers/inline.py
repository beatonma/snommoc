"""

"""

import logging

from rest_framework import serializers

from api.serializers import InlineSerializer
from repository.models import (
    Constituency,
    Person,
    Party,
    Bill,
)
from repository.models.geography import Town

log = logging.getLogger(__name__)


class InlineConstituencySerializer(InlineSerializer):
    class Meta:
        model = Constituency
        fields = [
            'parliamentdotuk',
            'name',
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
    class Meta:
        model = Party
        fields = [
            'parliamentdotuk',
            'name',
        ]


class InlineMemberSerializer(InlineSerializer):
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


class InlineBillSerializer(InlineSerializer):
    class Meta:
        model = Bill
        fields = [
            'parliamentdotuk',
            'title',
            'description',
            'date',
        ]
