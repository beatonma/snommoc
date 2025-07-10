import pytest


def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--skip_database",
        "--skip-database",
        dest="skip_database",
        action="store_true",
        default=False,
    )


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Raise exception if any live network calls are attempted during testing."""

    class NetworkCallInTest(Exception):
        pass

    def _raise_exception(call_path: str, *args, **kwargs):
        raise NetworkCallInTest(
            f"Network call attempted during tests: ({call_path}) {args} {kwargs}"
        )

    for x in [
        "requests.delete",
        "requests.get",
        "requests.head",
        "requests.options",
        "requests.patch",
        "requests.post",
        "requests.put",
        "requests.sessions.Session.request",
        "requests.sessions.Session.send",
    ]:
        monkeypatch.setattr(x, _raise_exception)
