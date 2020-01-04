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
from repository.models.contact_details import Links

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


class InlineMpSerializer(InlineSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name=f'{api_endpoints.MP}-detail',
        read_only=True
    )
    party = InlinePartySerializer()
    # name = serializers.CharField(source='person.name')
    constituency = InlineConstituencySerializer()

    class Meta:
        model = Person
        fields = [
            'name',
            'party',
            'constituency',
            'detail_url',
        ]


class LinksSerializer(DetailedSerializer):
    weblinks = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Links
        fields = [
            'email',
            'phone_constituency',
            'phone_parliament',
            'weblinks',
            'wikipedia',
        ]


class PartySerializer(DetailedSerializer):
    class Meta:
        model = Party
        fields = [
            'name',
            'short_name',
            'long_name',
        ]


class MpSerializer(DetailedSerializer):
    party = InlinePartySerializer()
    constituency = InlineConstituencySerializer()
    # name = serializers.CharField(source='person.name')

    # links = LinksSerializer()
    # countries_of_interest = serializers.StringRelatedField(many=True, read_only=True)
    # generic_interests = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Person
        fields = [
            'name',
            'parliamentdotuk',
            'theyworkforyou',
            'party',
            'constituency',
            # 'links',
            # 'countries_of_interest',
            # 'generic_interests',
        ]


class ConstituencySerializer(DetailedSerializer):
    mp = InlineMpSerializer()

    class Meta:
        model = Constituency
        fields = [
            'name',
            'mp',
            'start',
            'end',
        ]
