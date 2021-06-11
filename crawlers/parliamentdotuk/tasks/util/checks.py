from functools import reduce
from typing import List


class MissingFieldException(Exception):
    pass


def _has_required_fields(obj: dict, names: List[str]) -> bool:
    if obj is None:
        return False

    return reduce(lambda x, y: x and (y in obj), names)


# def check_required_fields(obj: dict, names: List[str]) -> None:
def check_required_fields(obj: dict, *names: str) -> None:
    """Raise MissingFieldException if the given object does not contain all of the provided field names."""
    if not _has_required_fields(obj, [*names]):
        missing_fields = ", ".join([x for x in names if x not in obj.keys()])
        raise MissingFieldException(
            f"Missing fields [{missing_fields}] from object {obj}"
        )
