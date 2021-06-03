import re
import datetime
from typing import (
    Dict,
    Optional,
    Callable,
)

from celery.utils.log import get_task_logger

from crawlers.parliamentdotuk.tasks.lda.endpoints import (
    MAX_PAGE_SIZE,
    PARAM_PAGE_SIZE,
    PARAM_PAGE,
)
from crawlers.parliamentdotuk.tasks.util.coercion import (
    coerce_to_date,
    coerce_to_int,
    coerce_to_list,
    coerce_to_str,
)
from notifications.models import TaskNotification
from crawlers.parliamentdotuk.tasks.network import get_json

log = get_task_logger(__name__)


def get_next_page_url(json_response) -> Optional[str]:
    try:
        return json_response.get("result").get("next")
    except AttributeError as e:
        log.warning(e)
        return None


def get_value(data: Dict, key: str) -> Optional[str]:
    """LDA data values are often but not always wrapped in a structure like
    {'label': { '_value': 'actual value' } }"""
    v = data.get(key)
    if isinstance(v, str):
        return v
    elif isinstance(v, Dict):
        if "_value" in v.keys():
            return v.get("_value")
        elif "label" in v.keys():
            try:
                return v.get("label").get("_value")
            except AttributeError:
                return None


def get_date(data: Dict, key: str) -> Optional[datetime.datetime]:
    return coerce_to_date(get_value(data, key))


def unwrap_value(data, key):
    """Many values are provided in an object wrapped with an array of length=1"""
    obj = data.get(key)
    if obj is None:
        return None
    elif isinstance(obj, list):
        return obj[0].get("_value")
    else:
        return obj.get("_value")


def unwrap_from_list(data, key):
    """Some values are returned as a single-item list - use this to get the item."""
    return data.get(key)[0]


def unwrap_str_from_list(data, key) -> str:
    """Some strings are returned as a single-item list - use this to get the string."""
    return coerce_to_str(unwrap_from_list(data, key))


def unwrap_value_str(data, key) -> str:
    return coerce_to_str(unwrap_value(data, key))


def unwrap_value_int(data, key) -> int:
    return coerce_to_int(unwrap_value(data, key))


def unwrap_value_date(data, key) -> datetime.date:
    return coerce_to_date(unwrap_value(data, key))


def get_str(data, key, default=None) -> Optional[str]:
    return coerce_to_str(data.get(key), default=default)


def get_int(data, key, default=None) -> Optional[int]:
    return coerce_to_int(data.get(key), default=default)


def get_list(data, key) -> list:
    return coerce_to_list(data.get(key))


def is_xml_null(obj: dict) -> bool:
    """Some values return an xml-schema-wrapped version of null.

    Return True iff the given object is an instance of xml-wrapped null.
    """
    return isinstance(obj, dict) and obj.get("@xsi:nil", "").lower() == "true"


def get_parliamentdotuk_id(about_url: str) -> Optional[int]:
    matches = re.findall(r".*?/([\d]+)$", about_url)
    if matches:
        return int(matches[0])


def get_nested_value(obj: dict, key: str):
    parts = key.split(".")
    parent = obj
    while len(parts) > 1:
        parent = parent.get(parts.pop(0))
        if parent is None or not isinstance(parent, dict):
            return None

    result = parent.get(parts.pop())
    if is_xml_null(result):
        return None
    return result


def _get_list_page_json(
    endpoint: str,
    page_number: int = 0,
    page_size: int = MAX_PAGE_SIZE,
    **kwargs,
) -> dict:
    return get_json(
        endpoint,
        params={
            PARAM_PAGE_SIZE: page_size,
            PARAM_PAGE: page_number,
        },
        **kwargs,
    )


def get_item_data(endpoint: str, **kwargs) -> Optional[Dict]:
    data = get_json(endpoint, **kwargs)
    return data.get("result").get("primaryTopic")


def update_model(
    endpoint_url: str,
    update_item_func: Callable[[Dict], Optional[str]],
    notification: TaskNotification,
    page_size=MAX_PAGE_SIZE,
    follow_pagination: bool = True,
    **kwargs,
) -> None:
    page_number = 0
    next_page = "nonnext-page-placeholder"

    while next_page is not None:
        data = _get_list_page_json(
            endpoint_url,
            page_number=page_number,
            page_size=page_size,
            **kwargs,
        )

        items = data.get("result").get("items")

        for item in items:
            try:
                update_item_func(item)
            except Exception as e:
                log.warning(f"Failed to update item: {e} {item}")
                notification.append(
                    f"Failed to read item for url={endpoint_url} page={page_number}"
                )
                notification.mark_as_failed(e)
                return

        page_number += 1
        next_page = get_next_page_url(data) if follow_pagination else None
