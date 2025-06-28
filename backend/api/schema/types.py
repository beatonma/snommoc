from typing import Annotated, Any, Literal
from urllib.parse import urljoin

from ninja import Schema
from pydantic import AfterValidator, Field
from pydantic.functional_validators import BeforeValidator
from pydantic_core import PydanticUndefined


def field(name: str, *, default: Any = PydanticUndefined) -> Field:
    return Field(default=default, alias=name)


type ParliamentId = int
type Name = str
type Title = str
type EmailAddress = str
type Url = str
type WikipediaPath = Annotated[
    str, AfterValidator(lambda path: urljoin("https://en.wikipedia.org/wiki/", path))
]


type PhoneNumber = Annotated[
    str,
    BeforeValidator(lambda x: x.as_national),  # Get string value from PhoneNumberField
]


def SplitString(separator: str):
    return Annotated[list[str], BeforeValidator(lambda x: x.split(separator))]


class ParliamentSchema(Schema):
    """A schema which has an associated parliament.uk API ID"""

    parliamentdotuk: ParliamentId


type DivisionVoteType = Literal["aye", "no", "did_not_vote"]
