import re
import datetime
from typing import (
    Any,
    Dict,
    Optional,
    Callable,
)

from celery.utils.log import get_task_logger

from crawlers.parliamentdotuk.tasks.lda.endpoints import (
    MAX_PAGE_SIZE,
    PARAM_PAGE_SIZE,
    PARAM_PAGE,
    debug_url,
)
from crawlers.parliamentdotuk.tasks.util.coercion import (
    coerce_to_boolean,
    coerce_to_date,
    coerce_to_int,
    coerce_to_list,
    coerce_to_str,
)
from notifications.models import TaskNotification
from crawlers.network import get_json
from crawlers.parliamentdotuk.tasks.lda import contract
from crawlers.parliamentdotuk.tasks.util.checks import MissingFieldException

log = get_task_logger(__name__)


def get_value(data: Dict, key: str) -> Optional[Any]:
    """
    LDA data values are often but not always wrapped in a structure like
    {
      'label': {
        '_value': 'actual value'
      }
    }

    Similarly, some values are wrapped in a single-item list.
    """
    if "." in key:
        v = _get_nested_value(data, key)
    else:
        v = data.get(key)

    if v is None:
        return None

    if isinstance(v, str) or isinstance(v, int) or isinstance(v, bool):
        return v

    elif isinstance(v, dict):
        if "_value" in v.keys():
            return v.get("_value")
        elif "label" in v.keys():
            try:
                return v["label"]["_value"]
            except AttributeError:
                return None

    elif isinstance(v, list):
        if len(v) == 1:
            item = v[0]
            if isinstance(item, dict):
                return v[0].get("_value")
            else:
                return item


def get_date(data: Dict, key: str) -> Optional[datetime.date]:
    return coerce_to_date(get_value(data, key))


def get_str(data, key, default=None) -> Optional[str]:
    return coerce_to_str(get_value(data, key), default=default)


def get_int(data, key, default=None) -> Optional[int]:
    return coerce_to_int(get_value(data, key), default=default)


def get_boolean(data, key, default=None) -> Optional[bool]:
    result = coerce_to_boolean(get_value(data, key))
    if result is None:
        return default
    else:
        return result


def get_list(data, key) -> list:
    return coerce_to_list(data.get(key))


def parse_parliamentdotuk_id(about_url: str) -> Optional[int]:
    matches = re.findall(r".*?/([\d]+)$", about_url)
    if matches:
        return int(matches[0])


def get_parliamentdotuk_id(obj: dict, key: str = contract.ABOUT) -> Optional[int]:
    try:
        return parse_parliamentdotuk_id(get_value(obj, key))
    except Exception as e:
        raise MissingFieldException(e)


def get_item_data(endpoint: str, **kwargs) -> Optional[Dict]:
    data = get_json(endpoint, **kwargs)
    return data["result"]["primaryTopic"]


def update_model(
    endpoint_url: str,
    update_item_func: Callable[[Dict], None],
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

        items = data["result"]["items"]

        for item in items:
            try:
                update_item_func(item)

            except MissingFieldException as e:
                notification.warning(
                    f"Item response is missing required data and will be skipped: "
                    f"[url={debug_url(endpoint_url, **{PARAM_PAGE:page_number, PARAM_PAGE_SIZE:page_size,})}] {e}"
                )
                continue

            except Exception as e:
                log.warning(f"Failed to update item: {e} {item}")

                notification.append(
                    f"Failed to read item for"
                    f"url={debug_url(endpoint_url, **{PARAM_PAGE:page_number, PARAM_PAGE_SIZE:page_size,})}"
                )
                notification.mark_as_failed(e)
                return

        page_number += 1
        next_page = _get_next_page_url(data) if follow_pagination else None


def _get_nested_value(obj: dict, key: str):
    parts = key.split(".")
    parent = obj
    while len(parts) > 1:
        parent = parent.get(parts.pop(0))
        if parent is None or not isinstance(parent, dict):
            return None

    result = parent.get(parts.pop())
    if _is_xml_null(result):
        return None
    return result


def _is_xml_null(obj: dict) -> bool:
    """Some values return an xml-schema-wrapped version of null.

    Return True iff the given object is an instance of xml-wrapped null.
    """
    return isinstance(obj, dict) and obj.get("@xsi:nil", "").lower() == "true"


def _get_next_page_url(json_response) -> Optional[str]:
    try:
        return json_response["result"]["next"]
    except (KeyError, AttributeError) as e:
        log.warning(e)
        return None


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
