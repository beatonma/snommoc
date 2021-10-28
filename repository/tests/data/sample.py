import dataclasses
import random
from typing import List, TypeVar

T = TypeVar("T")


def any_sample_of(available: List[T]) -> T:
    """T must be a @dataclass"""
    return dataclasses.replace(random.choice(available))
