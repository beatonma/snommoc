from typing import Annotated

from pydantic import AfterValidator
from repository.resolution.members import normalize_name

from .common import StringOrNone

__all__ = [
    "PersonName",
]

type PersonName = Annotated[StringOrNone, AfterValidator(normalize_name)]
