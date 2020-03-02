"""

"""

import logging

log = logging.getLogger(__name__)


class MockJsonResponse:
    def __init__(self, url, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        print(f'MOCK RESPONSE: {url}')

    def json(self):
        return self.json_data
