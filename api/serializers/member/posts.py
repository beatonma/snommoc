from rest_framework import serializers

from api.serializers.base import DetailedModelSerializer
from repository.models import (
    GovernmentPostMember,
    ParliamentaryPostMember,
    OppositionPostMember,
    Person,
)


class _PostMemberSerializer(DetailedModelSerializer):
    parliamentdotuk = serializers.IntegerField(source="post.parliamentdotuk")
    name = serializers.CharField(source="post.name")
    hansard = serializers.CharField(source="post.hansard_name")

    _fields = [
        "parliamentdotuk",
        "name",
        "hansard",
        "start",
        "end",
    ]


class _GovernmentPostMemberSerializer(_PostMemberSerializer):
    class Meta:
        model = GovernmentPostMember
        fields = _PostMemberSerializer._fields


class _ParliamentaryPostMemberSerializer(_PostMemberSerializer):
    class Meta:
        model = ParliamentaryPostMember
        fields = _PostMemberSerializer._fields


class _OppositionPostMemberSerializer(_PostMemberSerializer):
    class Meta:
        model = OppositionPostMember
        fields = _PostMemberSerializer._fields


class AllPostSerializer(DetailedModelSerializer):
    governmental = _GovernmentPostMemberSerializer(
        many=True,
        source="governmentpostmember_set",
    )
    parliamentary = _ParliamentaryPostMemberSerializer(
        many=True,
        source="parliamentarypostmember_set",
    )
    opposition = _OppositionPostMemberSerializer(
        many=True,
        source="oppositionpostmember_set",
    )

    class Meta:
        model = Person
        fields = [
            "governmental",
            "parliamentary",
            "opposition",
        ]
