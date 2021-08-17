"""
Exceptions that may be raised by [network.get_json].
"""


class HttpNoContent(Exception):
    pass


class HttpClientError(Exception):
    pass


class HttpServerError(Exception):
    pass
