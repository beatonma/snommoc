import json
from pathlib import Path
from unittest.mock import patch

from basetest.testcase import LocalTestCase


class OpenApiTestCase(LocalTestCase):
    """Provides self.patch() which returns JSON data from local file, depending
    on the requested URL. Mapping of URL to data file is defined in mock_response.

    e.g.
    with self.patch():
        function_which_makes_openapi_client_calls()
    """

    """File used to determine the CWD for resolution of mocked data."""
    file = __file__

    """
    key: URL
    value: path to a file containing the JSON content to be returned,
           relative to self.file
    """
    mock_response: dict[str, str]

    def patch(self):
        return patch(
            "crawlers.parliamentdotuk.tasks.openapi.openapi_client.get_json",
            side_effect=lambda url, *args, **kwargs: self._load_json_from_file(
                self.mock_response[url]
            ),
        )

    def _load_json_from_file(self, path: str):
        with open(Path(self.file).parent / path, "r") as f:
            return json.load(f)
