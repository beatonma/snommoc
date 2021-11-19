"""
Exceptions that may be raised by [network.get_json].
"""


class HttpError(Exception):
    status_code = None


class HttpNoContent(HttpError):
    status_code = 204


class HttpClientError(HttpError):
    def __init__(self, status_code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_code = status_code


class HttpServerError(HttpError):
    def __init__(self, status_code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_code = status_code
