import logging
import time
from typing import Optional

import requests
from django.conf import settings
from requests import sessions

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
            return cached

    log.info(encoded_url)
    with sessions.Session() as session:
        response = session.send(r)

    response.encoding = "utf-8-sig"
    time.sleep(1)  # Rate limiting

    data = response.json()
    if cache:
        cache.remember(encoded_url, data)

    return data
