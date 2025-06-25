from math import inf

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja.conf import settings as ninja_settings
from ninja.pagination import LimitOffsetPagination as NinjaLimitOffsetPagination
from pydantic import Field


class LimitOffsetPagination(NinjaLimitOffsetPagination):
    class Output(NinjaLimitOffsetPagination.Output):
        page_size: int
        previous: int | None
        next: int | None

    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: NinjaLimitOffsetPagination.Input,
        **params,
    ):
        offset = pagination.offset
        limit: int = min(pagination.limit, ninja_settings.PAGINATION_MAX_LIMIT)
        count = self._items_count(queryset)
        return {
            "items": queryset[offset : offset + limit],
            "count": count,
            "page_size": limit,
            **_get_next_previous(params.get("request"), offset, limit, count),
        }

    async def apaginate_queryset(
        self,
        queryset: QuerySet,
        pagination: NinjaLimitOffsetPagination.Input,
        **params,
    ):
        offset = pagination.offset
        limit: int = min(pagination.limit, ninja_settings.PAGINATION_MAX_LIMIT)
        count = await self._aitems_count(queryset)
        return {
            "items": queryset[offset : offset + limit],
            "count": count,
            "page_size": limit,
            **_get_next_previous(params.get("request"), offset, limit, count),
        }


def _get_next_previous(
    request: HttpRequest,
    offset: int,
    limit: int,
    count: int,
) -> dict[str, str | None]:
    _next = offset + limit
    if _next > count:
        _next = None

    _previous = max(0, offset - limit)
    if _previous == offset:
        _previous = None

    return {
        "next": _next,
        "previous": _previous,
    }


def offset_pagination(limit: int):
    _limit = limit

    class GeneratedLimitOffsetPagination(LimitOffsetPagination):
        class Input(LimitOffsetPagination.Input):
            limit: int = Field(
                _limit,
                ge=1,
                le=(
                    ninja_settings.PAGINATION_MAX_LIMIT
                    if ninja_settings.PAGINATION_MAX_LIMIT != inf
                    else None
                ),
            )
            offset: int = Field(0, ge=0)

    return GeneratedLimitOffsetPagination
