"""

"""

import logging

from rest_framework import serializers

from repository.models import (
    Mp,
    Constituency,
    Party,
)
from repository.models.contact_details import PersonalLinks

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


class PersonalLinksSerializer(DetailedSerializer):
    class Meta:
        model = PersonalLinks
        fields = [
            'email',
            'phone_constituency',
            'phone_parliament',
            'weblinks',
            'wikipedia',
        ]


class PersonalLinksRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        serializer = PersonalLinksSerializer(value.get_queryset()[0])
        return serializer.data


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
    contact = PersonalLinksRelatedField(read_only=True)

    class Meta:
        model = Mp
        fields = [
            'name',
            'parliamentdotuk',
            'theyworkforyou',
            'party',
            'constituency',
            'contact',
            'countries_of_interest',
            'political_interests',
        ]


class ConstituencySerializer(DetailedSerializer):
    mp = InlineMpSerializer()

    class Meta:
        model = Constituency
        fields = [
            'name',
            'mp',
        ]
