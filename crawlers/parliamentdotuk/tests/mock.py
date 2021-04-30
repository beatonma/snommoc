"""

"""

import logging

log = logging.getLogger(__name__)


class MockJsonResponse:
    def __init__(self, url, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.url = url
        print(f"MOCK RESPONSE: {url}")

    def json(self):
        return self.json_data

    def __str__(self):
        fields = "\n  ".join([self.url, str(self.status_code), str(self.json_data)])
        return f"MockJsonResponse: [\n{fields}\n]"
