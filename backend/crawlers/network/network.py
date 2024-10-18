import logging
from typing import Dict, Optional, Tuple, Union
from urllib.parse import urlparse

import requests
from common.network.rate_limit import rate_limit
from crawlers.network import JsonResponseCache
from crawlers.network.exceptions import HttpClientError, HttpNoContent, HttpServerError
from django.conf import settings
from rest_framework import status

log = logging.getLogger(__name__)


def _resolve_query(url: str, params: Dict | None) -> Tuple[str, Dict]:
    """Extract any existing params from `url` and add them to `params` for proper encoding"""
    query = {}
    params = params or {}

    if "?" in url:
        parsed = urlparse(url)
        parts = parsed.query.split("&")
        for part in parts:
            key, value = part.split("=")
            query[key] = value

    url = url.split("?")[0]
    query.update(params)
    return url, query


def get_json(
    url: str,
    params: Optional[dict] = None,
    cache: Optional[JsonResponseCache] = None,
    dangerous_encoded_params: bool = False,
    session: requests.Session = None,
    **kwargs,
) -> Union[dict, list]:
    """
    If `params` is not a dict, `dangerous_encoded_params` must also be True to avoid re-encoding by requests.Request.prepare().
    """

    if kwargs:
        log.warning(f"get_json: Unhandled kwargs {kwargs}")

    url, params = _resolve_query(url, params)

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

    if cache:
        cached = cache.get_json(encoded_url)
        if cached:
            log.info(f"[cached] {encoded_url}")
            return cached
    else:
        log.warning(f"No cache specified for call to '{url}'")

    with session or requests.Session() as session:
        response = session.send(r)
    log.info(f"GET {response.status_code} {encoded_url}")

    rate_limit()

    if response.status_code == status.HTTP_204_NO_CONTENT:
        raise HttpNoContent
    elif response.status_code >= 500:
        raise HttpServerError(response.status_code)
    elif response.status_code >= 400:
        raise HttpClientError(response.status_code)

    response.encoding = "utf-8-sig"

    data = response.json()
    if cache:
        cache.remember(encoded_url, data)

    return data
