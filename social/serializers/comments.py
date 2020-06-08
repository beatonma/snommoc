"""

"""

import logging

from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from social.models.comments import Comment
from social.models.token import UserToken
from social.views import contract

import bleach

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

    def validate_text(self, value):
        return bleach.clean(value, tags=[], attributes={}, styles=[], strip=True)

    class Meta:
        model = Comment
        fields = [
            contract.USER_TOKEN,
            contract.COMMENT_TEXT,
        ]

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        comment, _ = Comment.objects.get_or_create(
            user=UserToken.objects.get(token=validated_data.get(contract.USER_TOKEN)),
            target_id=self.target.pk,
            target_type=ContentType.objects.get_for_model(self.target),
            text=validated_data.get(contract.COMMENT_TEXT),
        )
        return comment
