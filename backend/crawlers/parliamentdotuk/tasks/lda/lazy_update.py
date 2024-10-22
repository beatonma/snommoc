import logging
from typing import Callable

from crawlers.network import JsonCache
from notifications.models import TaskNotification

log = logging.getLogger(__name__)


def lazy_update[
    T
](
    puk_model,
    update_func: Callable[[int, JsonCache | None], None],
    data: T,
    cache: JsonCache | None = None,
    notification: TaskNotification | None = None,
    force_update: bool = False,
) -> None:
    """
    Some data from the Parliament API are unlikely to change over time so we can reduce
    requests by skipping those that we already have.

    Sometimes we need to force a refresh of those data. AsyncCommand provides the -force flag
    for this purpose, which adds 'force_update=True' to the function kwargs. When this flag is
    set, the model should update from the Parliament API regardless of our existing data.

    :param puk_model: Class of the root model for updating e.g. ConstituencyResultDetail
    :param update_func: A function that accepts a parliamentdotuk ID and a JsonResponseCache
    :param data: A dictionary representing the JSON data of an item. See :func:`~lda_client.update_model`.
    :param cache: From required @json_cache decoration.
    :param force_update: From AsyncCommand
    """
    parliamentdotuk = getattr(data, "parliamentdotuk")

    if force_update:
        print(f"Forcing update with {update_func.__name__} for item #{parliamentdotuk}")
        update_func(parliamentdotuk, cache)

    else:
        try:
            puk_model.objects.get(parliamentdotuk=parliamentdotuk)
            return
        except puk_model.DoesNotExist:
            pass

        update_func(parliamentdotuk, cache)
