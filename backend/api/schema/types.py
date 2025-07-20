from typing import Annotated, Any, Literal
from urllib.parse import urljoin

from ninja import Schema
from phonenumber_field.phonenumber import PhoneNumber as PhoneNumberClass
from pydantic import AfterValidator, Field, WrapValidator
from pydantic.functional_validators import BeforeValidator
from pydantic_core import PydanticUndefined
from pydantic_core.core_schema import ValidatorFunctionWrapHandler
from repository.models import House as HouseModel

__all__ = [
    "field",
    "AdministrativeName",
    "DivisionVoteType",
    "EmailAddress",
    "House",
    "PersonName",
    "ParliamentId",
    "ParliamentSchema",
    "PhoneNumber",
    "Safe",
    "Url",
    "WikipediaPath",
]

from repository.models.houses import HouseType


def field(name: str, *, default: Any = PydanticUndefined) -> Field:
    return Field(default=default, alias=name)


# Common data - some are simple type aliases but are used to simplify
# implementation of any future custom validation rules.

type EmailAddress = str
type PersonName = str

"""Name of a non-person: e.g. a constituency, party, organisation..."""
type AdministrativeName = str
type ParliamentId = int
type Title = str
type Url = str
type DivisionVoteType = Literal["aye", "no", "did_not_vote"]
type House = Annotated[HouseType, BeforeValidator(_house_name)]
type PhoneNumber = Annotated[str, BeforeValidator(_phone_number)]
type WikipediaPath = Annotated[str, AfterValidator(_wikipedia_path)]

"""Wraps another validator. If that validator raises an exception, return None."""
type Safe[T] = Annotated[T | None, WrapValidator(_try_catch_none)]


def _try_catch_none[T](value: Any, handler: ValidatorFunctionWrapHandler) -> T | None:
    try:
        return handler(value)
    except:
        return None


def _wikipedia_path(path: str) -> str:
    return urljoin("https://en.wikipedia.org/wiki/", path)


def _house_name(house: HouseModel) -> str:
    return house.name


def _phone_number(phone: PhoneNumberClass):
    return phone.as_national


def _administrative_name(name: str) -> str:
    return name


class ParliamentSchema(Schema):
    """A schema which has an associated parliament.uk API ID"""

    parliamentdotuk: ParliamentId
