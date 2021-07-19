import logging
from typing import Optional
from urllib.parse import urlparse

import requests
from django.conf import settings
from requests import sessions

from common.network.rate_limit import rate_limit
from crawlers.network import JsonResponseCache

log = logging.getLogger(__name__)


def get_json(
    url: str,
    params: Optional[dict] = None,
    cache: Optional[JsonResponseCache] = None,
    dangerous_encoded_params: bool = False,
    **kwargs,
) -> dict:
    """
    If `params` is not a dict, `dangerous_encoded_params` must also be True to avoid re-encoding by requests.Request.prepare().
    """
    req = requests.Request(
        "GET",
        url,
        headers=settings.HTTP_REQUEST_HEADERS_JSON,
        params=params,
    )
    r = req.prepare()

    if dangerous_encoded_params is True and isinstance(params, str):
        encoded_url = urlparse(r.url)
        r.url = encoded_url.geturl().replace(encoded_url.query, params)

    encoded_url = r.url
    print(f"URL {encoded_url}")

    if cache:
        cached = cache.get_json(encoded_url)
        print("CACHED", cached)
        if cached:
            log.info(f"[cached] {encoded_url}")
            return cached
    else:
        log.warning(f"No cache specified for call to '{url}'")

    log.info(f"[using network] {encoded_url}")
    with sessions.Session() as session:
        response = session.send(r)

    response.encoding = "utf-8-sig"
    rate_limit()

    data = response.json()
    if cache:
        cache.remember(encoded_url, data)

    return data
