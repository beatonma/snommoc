import uuid

from django.db import models
from social.models import Comment, Vote
from social.models.mixins import get_target_kwargs
from social.models.token import UserToken


def create_sample_usertoken(
    username=None,
    token=uuid.uuid4,
    **kwargs,
) -> UserToken:
    if username is None:
        username = uuid.uuid4().hex[:6]

    if callable(token):
        token = token()

    return UserToken.objects.create(
        username=username,
        token=token,
        provider_account_id=uuid.uuid4(),
        **kwargs,
    )


def create_sample_comment(
    target: models.Model,
    user: UserToken,
    text=uuid.uuid4,
    **kwargs,
) -> Comment:
    if callable(text):
        text = str(text())

    return Comment.objects.create(
        target=target,
        user=user,
        text=text,
        **kwargs,
    )


def create_sample_vote(
    target: models.Model,
    user: UserToken,
    vote_type_name: str,
    **kwargs,
) -> Vote:
    return Vote.objects.create(
        user=user,
        **get_target_kwargs(target),
        vote_type=vote_type_name,
        **kwargs,
    )
