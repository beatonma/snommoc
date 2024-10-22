"""Common schema types for all data sources"""

from typing import Annotated

from pydantic import AfterValidator

__all__ = [
    "NullableString",
]

"""Return null if the parsed value is falsy."""
type FalsyNullable[T] = Annotated[
    T | None, AfterValidator(lambda obj: obj if obj else None)
]


"""Coerce empty strings as None."""
NullableString = FalsyNullable[str]
