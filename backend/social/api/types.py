from typing import Annotated

import nh3
from pydantic import AfterValidator, Field
from social.models import UserToken
from social.validation.username import BlockedUsername, is_username_blocked

type SanitizedText = Annotated[
    str,
    AfterValidator(sanitize_text),
]


def sanitize_text(text: str) -> str:
    return nh3.clean(text, tags=set(), attributes={}).strip()


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
