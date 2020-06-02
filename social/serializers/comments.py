"""

"""

import logging

from rest_framework import serializers

from social.models.comments import Comment
from social.models.token import UserToken

log = logging.getLogger(__name__)


class CommentSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(source='text')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Comment
        fields = [
            'username',
            'comment',
            'created_on',
            'modified_on',
        ]


class PostCommentSerializer(serializers.ModelSerializer):
    def __init__(self, target, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = target

    # comment = serializers.CharField(source='text')
    token = serializers.CharField()

    class Meta:
        model = Comment
        fields = [
            'token',
            'text',
        ]

    def create(self, validated_data):
        log.info(f'validated: {validated_data}')
        return Comment.objects.create(
            user=UserToken.objects.get(token=validated_data.get('token')),
            text=validated_data.get('text'),
            target=self.target
        )
