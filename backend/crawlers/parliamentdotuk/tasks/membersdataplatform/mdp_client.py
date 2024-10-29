from typing import Callable

from crawlers.context import TaskContext
from crawlers.network import get_json

from . import schema

type ItemFunc[T: schema.Member] = Callable[[T, TaskContext], None]


def foreach(
    url: str,
    item_func: ItemFunc,
    context: TaskContext,
) -> None:
    notification = context.notification
    response = get_json(url, cache=context.cache, session=context.session)

    members = schema.MemberListResponse.model_validate(response).members

    for member in members:
        try:
            item_func(member, context)
        except Exception as e:
            notification.warning(
                f"Failed to update member=[{member}…][{notification.html_link(url)}]: {e}"
            )
            notification.mark_as_failed(e)
            return


def once(
    url: str,
    item_func: ItemFunc,
    context: TaskContext,
) -> None:
    response = get_json(url, cache=context.cache, session=context.session)
    member = schema.MemberResponse.model_validate(response).member
    item_func(member, context)
