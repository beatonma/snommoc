from datetime import datetime
from typing import Annotated, Any, Literal, Type

import nh3
from django.shortcuts import get_object_or_404
from ninja import Schema
from pydantic import AfterValidator, Field
from pydantic_core import PydanticUndefined
from repository.models import Bill, CommonsDivision, Constituency, LordsDivision, Person
from repository.models.mixins import SocialMixin
from social.models import UserToken, Vote

from ..models.mixins import GenericTargetMixin
from .errors import BadUserToken


def field(
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


def resolve_user_token(token: str | None):
    if token is None:
        return None

    try:
        return UserToken.objects.get(token=token, enabled=True)
    except UserToken.DoesNotExist:
        raise BadUserToken()


def sanitize_text(text: str) -> str:
    return nh3.clean(text, tags=set(), attributes={}).strip()


type SanitizedText = Annotated[
    str,
    AfterValidator(sanitize_text),
    Field(min_length=1, max_length=240),
]


class InteractionSchema(Schema):
    private_target_model: InteractionTargetKey = field("target")
    private_target_id: int = field("target_id")
    private_user_token: str = field("token")

    def resolve_target_or_404(self):
        return resolve_target_or_404(
            self.private_target_model,
            self.private_target_id,
        )

    def resolve_target_kwargs(self) -> dict:
        return GenericTargetMixin.get_target_kwargs(self.resolve_target_or_404())

    def resolve_user_token(self):
        return resolve_user_token(self.private_user_token)


class CreateVote(InteractionSchema):
    vote_type: Vote.VoteTypeChoices = field("vote")


class DeleteVote(InteractionSchema):
    pass


class CreateComment(InteractionSchema):
    private_dangerous_unsanitized_text: str = field("text")
    text: SanitizedText

    def is_flagged(self):
        return self.private_dangerous_unsanitized_text != self.text


class Votes(Schema):
    pass


class Comment(Schema):
    username: str = field("user.username")
    text: str
    created_on: datetime
    modified_on: datetime


class SocialContent(Schema):
    title: str
    comments: list[Comment]
    votes: dict[Vote.VoteTypeChoices, int]
    user_vote: Vote.VoteTypeChoices | None
