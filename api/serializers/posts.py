import logging

from rest_framework import serializers

from api.serializers.base import DetailedModelSerializer
from repository.models import (
    GovernmentPostMember,
    ParliamentaryPostMember,
    OppositionPostMember,
    Person,
)

log = logging.getLogger(__name__)


class PostMemberSerializer(DetailedModelSerializer):
    parliamentdotuk = serializers.IntegerField(source="post.parliamentdotuk")
    name = serializers.CharField(source="post.name")
    hansard = serializers.CharField(source="post.hansard_name")


class PostMetaClass:
    fields = [
        "parliamentdotuk",
        "name",
        "hansard",
        "start",
        "end",
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


class AllPostSerializer(DetailedModelSerializer):
    governmental = GovernmentPostMemberSerializer(
        many=True,
        source="governmentpostmember_set",
    )
    parliamentary = ParliamentaryPostMemberSerializer(
        many=True,
        source="parliamentarypostmember_set",
    )
    opposition = OppositionPostMemberSerializer(
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
