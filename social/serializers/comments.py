"""

"""

import logging

from rest_framework import serializers

from social.models.comments import Comment
from social.models.token import UserToken
from social.views import contract

log = logging.getLogger(__name__)


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Comment
        fields = [
            contract.USER_NAME,
            contract.COMMENT_TEXT,
            'created_on',
            'modified_on',
        ]


class PostCommentSerializer(serializers.ModelSerializer):
    def __init__(self, target, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = target

    token = serializers.CharField()

    class Meta:
        model = Comment
        fields = [
            contract.USER_TOKEN,
            contract.COMMENT_TEXT,
        ]

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        log.info(f'validated: {validated_data}')
        return Comment.objects.create(
            user=UserToken.objects.get(token=validated_data.get(contract.USER_TOKEN)),
            target=self.target,
            text=validated_data.get(contract.COMMENT_TEXT),
        )