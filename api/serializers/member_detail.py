"""

"""

import logging

from rest_framework import serializers

from api.serializers.detail import DetailedSerializer
from api.serializers.inline import (
    InlinePartySerializer,
    InlineConstituencySerializer,
    InlineTownSerializer,
)
from repository.models import (
    GovernmentPostMember,
    ParliamentaryPostMember,
    OppositionPostMember,
    Person,
    PhysicalAddress,
    WebAddress,
)

log = logging.getLogger(__name__)

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


class PhysicalAddressSerializer(DetailedSerializer):
    class Meta:
        model = PhysicalAddress
        fields = [
            'description',
            'address',
            'postcode',
            'phone',
            'fax',
            'email',
        ]


class WebAddressSerializer(DetailedSerializer):
    class Meta:
        model = WebAddress
        fields = [
            'description',
            'url',
        ]


class AddressSerializer(DetailedSerializer):
    physical = PhysicalAddressSerializer(many=True, source='physicaladdress_set')
    web = WebAddressSerializer(many=True, source='webaddress_set')

    class Meta:
        model = Person

        fields = [
            'name',
            'parliamentdotuk',
            'physical',
            'web',
        ]


class PostMemberSerializer(DetailedSerializer):
    parliamentdotuk = serializers.IntegerField(source='post.parliamentdotuk')
    name = serializers.CharField(source='post.name')
    hansard = serializers.CharField(source='post.hansard_name')


class PostMetaClass:
    fields = [
        'parliamentdotuk',
        'name',
        'hansard',
    ]


class GovernmentPostMemberSerializer(PostMemberSerializer):
    class Meta(PostMetaClass):
        model = GovernmentPostMember


class ParliamentaryPostMemberSerializer(PostMemberSerializer):
    class Meta(PostMetaClass):
        model = ParliamentaryPostMember


class OppositionPostMemberSerializer(PostMemberSerializer):
    class Meta(PostMetaClass):
        model = OppositionPostMember


class AllPostSerializer(DetailedSerializer):
    governmental = GovernmentPostMemberSerializer(
        many=True,
        source='governmentpostmember_set',
    )
    parliamentary = ParliamentaryPostMemberSerializer(
        many=True,
        source='parliamentarypostmember_set',
    )
    opposition = OppositionPostMemberSerializer(
        many=True,
        source='oppositionpostmember_set',
    )

    class Meta:
        model = Person
        fields = [
            'governmental',
            'parliamentary',
            'opposition',
        ]


class DeclaredInterestSerializer(DetailedSerializer):
    pass
