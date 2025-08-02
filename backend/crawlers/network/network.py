import logging
from urllib.parse import urlparse, urlunparse

import requests
from django.conf import settings

from api import status
from common.network.rate_limit import rate_limit
from crawlers.network import JsonCache
from crawlers.network.exceptions import HttpClientError, HttpNoContent, HttpServerError

log = logging.getLogger(__name__)


def _resolve_query(url: str, params: dict | None) -> tuple[str, dict]:
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
    params: dict | None = None,
    cache: JsonCache | None = None,
    dangerous_encoded_params: str | None = None,
    session: requests.Session = None,
) -> dict | list:
    url, params = _resolve_query(url, params)

    req = requests.Request(
        "GET",
        url,
        headers=settings.HTTP_REQUEST_HEADERS_JSON,
        params=params,
    )
    r = req.prepare()

    if isinstance(dangerous_encoded_params, str):
        scheme, netloc, url, params, query, fragment = urlparse(r.url)
        r.url = str(
            urlunparse(
                [scheme, netloc, url, params, dangerous_encoded_params, fragment]
            )
        )

    encoded_url = r.url

    if cache:
        cached = cache.get_json(encoded_url)
        if cached:
            log.info(rf"\[[cyan]cache[/]] {encoded_url}", extra={"markup": True})
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
