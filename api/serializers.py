"""

"""

import logging

from rest_framework import serializers

from repository.models import (
    Mp,
    Constituency,
    Party,
)

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
        view_name='party-detail',
        read_only=True
    )

    class Meta:
        model = Party
        fields = [
            'name',
            'detail_url',
        ]


class InlineMpSerializer(InlineSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='mp-detail',
        read_only=True
    )
    party = InlinePartySerializer()

    class Meta:
        model = Mp
        fields = [
            'name',
            'party',
            'detail_url',
        ]


class InlineConstituencySerializer(InlineSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='constituency-detail',
        read_only=True
    )

    class Meta:
        model = Constituency
        fields = [
            'name',
            'detail_url',
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

    class Meta:
        model = Mp
        fields = [
            'name',
            'party',
            'constituency',
        ]


class ConstituencySerializer(DetailedSerializer):
    mp = InlineMpSerializer()

    class Meta:
        model = Constituency
        fields = [
            'name',
            'mp',
        ]
