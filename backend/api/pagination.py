from math import inf

from ninja import Field, Schema
from ninja.conf import settings
from ninja.pagination import LimitOffsetPagination


def offset_pagination(limit: int):
    _limit = limit

    class GeneratedLimitOffsetPagination(LimitOffsetPagination):
        class Input(Schema):
            limit: int = Field(
                _limit,
                ge=1,
                le=(
                    settings.PAGINATION_MAX_LIMIT
                    if settings.PAGINATION_MAX_LIMIT != inf
                    else None
                ),
            )
            offset: int = Field(0, ge=0)

    return GeneratedLimitOffsetPagination
