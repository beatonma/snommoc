from typing import Annotated, Any

from ninja import Schema
from pydantic import Field
from pydantic.functional_validators import BeforeValidator
from pydantic_core import PydanticUndefined


def field(name: str, *, default: Any = PydanticUndefined) -> Field:
    return Field(default=default, alias=name)


type ParliamentId = int
type Name = str
type Title = str
type EmailAddress = str
type Url = str
type WikipediaPath = str


type PhoneNumber = Annotated[
    str,
    BeforeValidator(lambda x: x.as_national),  # Get string value from PhoneNumberField
]


class MiniSchema(Schema):
    """A minimal schema with only the most important fields,
    for use when embedding in another schema.

    The existence of a `MiniSchema` implementation implies an
    associated `FullSchema` implementation. If that is not the
    case, just extend `ninja.Schema` directly."""

    pass


class FullSchema(Schema):
    """A complete schema with all fields that may be needed.

    The existence of a `FullSchema` implementation implies an
    associated `MiniSchema` implementation. If that is not the
    case, just extend `ninja.Schema` directly."""

    pass


class ParliamentSchema(Schema):
    """A schema which has an associated parliament.uk API ID"""

    parliamentdotuk: ParliamentId
