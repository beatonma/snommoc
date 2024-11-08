from datetime import datetime
from typing import Any, Literal, Type

from django.shortcuts import get_object_or_404
from ninja import Schema
from pydantic import Field
from pydantic_core import PydanticUndefined
from repository.models import Bill, CommonsDivision, Constituency, LordsDivision, Person
from repository.models.mixins import SocialMixin
from social.models import UserToken, Vote

from ..models.mixins import GenericTargetMixin
from . import types
from .errors import BadUserToken


def _field(
    alias: str,
    *,
    default: Any = PydanticUndefined,
    default_factory: Any = PydanticUndefined,
) -> Any:
    return Field(
        validation_alias=alias,
        default=default,
        default_factory=default_factory,
    )


type InteractionTarget = Type[SocialMixin]
type InteractionTargetKey = Literal[
    "person",
    "bill",
    "commons_division",
    "lords_division",
    "constituency",
]
interaction_target_map: dict[InteractionTargetKey, InteractionTarget] = {
    "person": Person,
    "bill": Bill,
    "commons_division": CommonsDivision,
    "lords_division": LordsDivision,
    "constituency": Constituency,
}


def resolve_target_or_404(target_model: InteractionTargetKey, target_id: int):
    return get_object_or_404(
        interaction_target_map[target_model],
        pk=target_id,
    )


def resolve_user_token(token: str | None, **kwargs):
    if token is None:
        return None

    try:
        return UserToken.objects.get(token=token, enabled=True, **kwargs)
    except UserToken.DoesNotExist:
        raise BadUserToken()


class _UserTokenSchema(Schema):
    private_user_token: str = _field("token")

    def resolve_user_token(self, **kwargs):
        return resolve_user_token(self.private_user_token, **kwargs)


class _InteractionSchema(_UserTokenSchema):
    private_target_model: InteractionTargetKey = _field("target")
    private_target_id: int = _field("target_id")

    def resolve_target_or_404(self):
        return resolve_target_or_404(
            self.private_target_model,
            self.private_target_id,
        )

    def resolve_target_kwargs(self) -> dict:
        return GenericTargetMixin.get_target_kwargs(self.resolve_target_or_404())


class CreateVoteRequest(_InteractionSchema):
    vote_type: Vote.VoteTypeChoices = _field("vote")


class DeleteVoteRequest(_InteractionSchema):
    pass


class CreateCommentRequest(_InteractionSchema):
    private_dangerous_unsanitized_text: str = _field("text")
    text: types.CommentText

    def is_flagged(self):
        return self.private_dangerous_unsanitized_text != self.text


class Comment(Schema):
    username: str = _field("user.username")
    text: str
    created_on: datetime
    modified_on: datetime


class SocialContentResponse(Schema):
    title: str
    comments: list[Comment]
    votes: dict[Vote.VoteTypeChoices, int]
    user_vote: Vote.VoteTypeChoices | None


class UserAccount(Schema):
    username: str


class RenameAccountRequest(_UserTokenSchema):
    username: str
    new_username: types.NewUsername


class DeleteAccountRequest(_UserTokenSchema):
    pass


class GoogleAuthRequest(Schema):
    """Received from a client who wants to sign in using Google oauth2"""

    encoded_oauth_token: str


class JsonWebToken(Schema):
    audience: str = _field("aud")
    issuer: str = _field("iss")
    user_id: str = _field("sub")
    expires_at: datetime = _field("exp")
    not_before: datetime = _field("nbf")
    issued_at: datetime = _field("iat")


class UserLoginResponse(UserAccount):
    """When user signs in successfully, return their basic account info and UserToken"""

    token: str
