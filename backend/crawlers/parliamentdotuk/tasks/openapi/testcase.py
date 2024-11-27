import json
import logging
from pathlib import Path
from unittest.mock import patch

from basetest.testcase import LocalTestCase

log = logging.getLogger(__name__)


class OpenApiTestCase(LocalTestCase):
    """Provides cls.patch() which returns JSON data from a local file, depending
    on the requested URL. Mapping of URL to data file is defined in mock_response.

    Example usage:
        @classmethod
        def setUpTestData(cls):
            with cls.patch():
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

    @classmethod
    def patch(cls):
        return patch(
            "crawlers.parliamentdotuk.tasks.openapi.openapi_client.get_json",
            side_effect=lambda url, *args, **kwargs: cls._load_json_from_file(
                cls.mock_response[url]
            ),
        )

    @classmethod
    def _load_json_from_file(cls, path: str):
        with open(Path(cls.file).parent / path, "r") as f:
            log.info(f"Loaded mock data from {path}")
            return json.load(f)
