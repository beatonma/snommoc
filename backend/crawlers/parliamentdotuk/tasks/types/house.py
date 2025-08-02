from typing import Annotated, cast

from pydantic import AfterValidator, BeforeValidator

from repository.models.houses import HOUSE_OF_COMMONS, HOUSE_OF_LORDS, HouseType

from .common import StringOrNone

__all__ = [
    "House",
]

HOUSE_ID_MAP: dict[int, HouseType] = {
    1: HOUSE_OF_COMMONS,
    2: HOUSE_OF_LORDS,
}
HOUSES: list[HouseType] = [HOUSE_OF_COMMONS, HOUSE_OF_LORDS]


def _house_id_to_name(value):
    if isinstance(value, int):
        return HOUSE_ID_MAP.get(value)
    return value


def _as_housetype(value: str | None) -> HouseType | None:
    if isinstance(value, str):
        value = value.capitalize()
        if value in HOUSES:
            return cast(HouseType, value)


type House = Annotated[
    StringOrNone,
    BeforeValidator(_house_id_to_name),
    AfterValidator(_as_housetype),
]
