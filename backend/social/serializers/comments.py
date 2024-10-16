import nh3
from rest_framework import serializers
from social.models.comments import Comment
from social.models.mixins import get_target_kwargs
from social.models.token import UserToken
from social.views import contract


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = Comment
        fields = [
            contract.USER_NAME,
            contract.COMMENT_TEXT,
            "created_on",
            "modified_on",
        ]


class PostCommentSerializer(serializers.ModelSerializer):
    def __init__(self, target, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = target

    token = serializers.CharField()

    def validate(self, data):
        original_text = data[contract.COMMENT_TEXT]
        stripped_text = nh3.clean(original_text, tags=set(), attributes={}).strip()

        if original_text != stripped_text:
            data[contract.FLAGGED] = True
            data[contract.COMMENT_TEXT] = stripped_text

        return data

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
            **get_target_kwargs(self.target),
            text=validated_data.get(contract.COMMENT_TEXT),
            flagged=validated_data.get(contract.FLAGGED, False),
        )
        return comment
