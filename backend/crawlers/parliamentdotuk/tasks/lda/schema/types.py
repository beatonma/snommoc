import re
from typing import Annotated

from crawlers.parliamentdotuk.tasks.types import CoercedDate
from pydantic import BeforeValidator

__all__ = [
    "NestedDate",
    "NestedValue",
    "ParliamentId",
    "VoteCount",
]


type ParliamentId = Annotated[
    int,
    BeforeValidator(
        lambda about_url: re.match(r".*/(\d+)$", about_url)[1],
    ),
]


type VoteCount = Annotated[int, BeforeValidator(lambda obj: obj[0]["_value"])]
type NestedValue[T] = Annotated[T, BeforeValidator(lambda obj: obj["_value"])]
NestedDate = NestedValue[CoercedDate]
NestedStr = NestedValue[str]
