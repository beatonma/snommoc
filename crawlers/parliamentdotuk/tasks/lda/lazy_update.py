from typing import Optional, Callable

from crawlers.network import JsonResponseCache
from crawlers.parliamentdotuk.tasks.lda.lda_client import get_parliamentdotuk_id


def lazy_update(
    puk_model,
    update_func: Callable[[int, Optional[JsonResponseCache]], None],
    json_data: dict,
    **kwargs,
) -> None:
    """
    Some data from the Parliament API are unlikely to change over time so we can reduce
    requests by skipping those that we already have.

    Sometimes we need to force a refresh of those data. AsyncCommand provides the -force flag
    for this purpose, which adds 'force_update=True' to the function kwargs. When this flag is
    set, the model should update from the Parliament API regardless of our existing data.

    :param puk_model: Class of the root model for updating e.g. ConstituencyResultDetail
    :param update_func: A function that accepts a parliamentdotuk ID and a JsonResponseCache
    :param json_data: A dictionary representing the JSON data of an item. See :func:`~lda_client.update_model`.
    :param kwargs: This will typically include a cache definition from @json_cache decoration,
                   and possibly force_cache from AsyncCommand.
    """
    puk = get_parliamentdotuk_id(json_data)
    cache = kwargs.get("cache")

    if kwargs.get("force_update"):
        print(f"Forcing update with {update_func.__name__} for item #{puk}")
        update_func(puk, cache)

    else:
        try:
            puk_model.objects.get(parliamentdotuk=puk)
            return
        except puk_model.DoesNotExist:
            pass

        update_func(puk, cache)
