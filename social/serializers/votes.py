from rest_framework import serializers

from social.models.mixins import get_target_kwargs
from social.models.token import UserToken
from social.models.votes import (
    Vote,
    VoteType,
)
from social.views import contract


class PostVoteSerializer(serializers.Serializer):
    def __init__(self, target, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = target

    token = serializers.CharField()
    vote = serializers.CharField(max_length=16)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        vote_type, _ = VoteType.objects.get_or_create(
            name=validated_data.get(contract.VOTE_TYPE)
        )
        vote, _ = Vote.objects.update_or_create(
            user=UserToken.objects.get(token=validated_data.get(contract.USER_TOKEN)),
            **get_target_kwargs(self.target),
            defaults={
                "vote_type": vote_type,
            }
        )
        return vote
