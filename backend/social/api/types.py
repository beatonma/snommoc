from typing import Annotated

from pydantic import AfterValidator, Field
from social.models import UserToken
from social.validation.username import BlockedUsername, is_username_blocked
from util.strings import sanitize_html

type SanitizedText = Annotated[
    str,
    AfterValidator(sanitize_html),
]


type CommentText = Annotated[
    SanitizedText,
    Field(min_length=1, max_length=240),
]


def validate_username(name: str) -> str:
    if is_username_blocked(name):
        raise BlockedUsername(name)

    UserToken.username_validator()(name)
    return name


type NewUsername = Annotated[SanitizedText, AfterValidator(validate_username)]
