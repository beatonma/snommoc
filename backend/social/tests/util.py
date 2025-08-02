import uuid

from django.db import models
from django.urls import reverse_lazy

from social.api import api
from social.models import Comment, OAuthToken, Vote
from social.models.mixins import get_target_kwargs
from social.models.token import UserToken


def reverse_api(view_name: str, *args, **kwargs):
    return reverse_lazy(f"{api.urls_namespace}:{view_name}", args=args, kwargs=kwargs)


def create_sample_usertoken(
    username=None,
    token=uuid.uuid4,
    oauth: OAuthToken | None = None,
    **kwargs,
) -> UserToken:
    if username is None:
        username = uuid.uuid4().hex[:6]

    if callable(token):
        token = token()

    return UserToken.objects.create(
        username=username,
        token=token,
        oauth_session=oauth or create_oauth_session(),
        **kwargs,
    )


def create_oauth_session(
    provider: str = "test-provider",
    user_id=uuid.uuid4,
) -> OAuthToken:
    if callable(user_id):
        user_id = str(user_id())
    session, _ = OAuthToken.objects.get_or_create(
        provider=provider,
        user_id=user_id,
    )
    return session


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
