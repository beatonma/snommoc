import logging
import time
from typing import Optional

import requests
from django.conf import settings
from requests import sessions

from common.network.rate_limit import rate_limit
from crawlers.parliamentdotuk.tasks.network import JsonResponseCache

log = logging.getLogger(__name__)


def get_json(
    url: str,
    params: Optional[dict] = None,
    cache: Optional[JsonResponseCache] = None,
    **kwargs,
) -> dict:
    req = requests.Request(
        "GET",
        url,
        headers=settings.HTTP_REQUEST_HEADERS_JSON,
        params=params,
    )
    r = req.prepare()
    encoded_url = r.url

    if cache:
        cached = cache.get_json(encoded_url)
        if cached:
            log.info(f"[cached] {encoded_url}")
            return cached
    else:
        log.warning(f"No cache specified for call to '{url}'")

    log.info(encoded_url)
    with sessions.Session() as session:
        response = session.send(r)

    response.encoding = "utf-8-sig"
    rate_limit()

    data = response.json()
    if cache:
        cache.remember(encoded_url, data)

    return data
