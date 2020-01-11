"""
Model serializers
"""

import logging

from rest_framework import serializers

from api import endpoints as api_endpoints
from repository.models import (
    Constituency,
    Party,
    Person,
)
from repository.models.geography import Town

log = logging.getLogger(__name__)


class DetailedSerializer(serializers.HyperlinkedModelSerializer):
    """Return all details about the object."""
    pass


class InlineSerializer(serializers.HyperlinkedModelSerializer):
    """Return basic data about the object with a link for further
    details if required."""
    pass


class InlinePartySerializer(InlineSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name=f'{api_endpoints.PARTY}-detail',
        read_only=True
    )

    class Meta:
        model = Party
        fields = [
            'name',
            'detail_url',
        ]


class InlineConstituencySerializer(InlineSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name=f'{api_endpoints.CONSTITUENCY}-detail',
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


class InlineMemberSerializer(InlineSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name=f'{api_endpoints.MEMBER}-detail',
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


class PartySerializer(DetailedSerializer):

    class Meta:
        model = Party
        fields = [
            'name',
            'short_name',
            'long_name',
            'homepage',
            'year_founded',
            'wikipedia',
        ]


class MemberSerializer(DetailedSerializer):
    party = InlinePartySerializer()
    constituency = InlineConstituencySerializer()
    place_of_birth = InlineTownSerializer(source='town_of_birth')

    class Meta:
        model = Person
        fields = [
            'name',
            'full_title',
            'parliamentdotuk',
            'theyworkforyou',
            'party',
            'constituency',
            'is_mp',
            'is_lord',
            'age',
            'gender',
            'place_of_birth',
        ]


class ConstituencySerializer(DetailedSerializer):
    mp = InlineMemberSerializer()

    class Meta:
        model = Constituency
        fields = [
            'name',
            'mp',
            'start',
            'end',
        ]
