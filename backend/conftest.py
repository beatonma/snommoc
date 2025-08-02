import os
import re
from pathlib import Path

import pytest
from django.conf import settings

"""Populated in pytest_configure"""
DISABLED_INTERNAL_APPS: list[str]


def discover_internal_apps():
    base_dir = Path(__file__).parent
    for cwd, dirs, files in base_dir.walk():
        if "env" in dirs:
            dirs.remove("env")

        if "migrations" in dirs and "__init__.py" in files:
            yield str(cwd.relative_to(base_dir).as_posix()).replace("/", ".")


def pytest_configure(config):
    global DISABLED_INTERNAL_APPS
    internal_apps = list(discover_internal_apps())
    DISABLED_INTERNAL_APPS = [
        x for x in internal_apps if x not in settings.INSTALLED_APPS
    ]
    if DISABLED_INTERNAL_APPS:
        print(
            f"Tests will be skipped for apps not included in settings.INSTALLED_APPS: {DISABLED_INTERNAL_APPS}"
        )


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


class SkippedModule(pytest.Module):
    FUNC_PATTERN = re.compile(r"\s*def (?P<funcname>\w+)")

    def __init__(self, path: Path, parent: pytest.Collector, reason: str, **kwargs):
        super().__init__(path=path, parent=parent, **kwargs)
        self.reason = reason

    def _getobj(self):
        return SkippedObj()

    def collect(self):
        values = []
        with self.path.open("r", encoding="utf-8") as f:
            for lineno, line in enumerate(f.readlines()):
                if match := self.__class__.FUNC_PATTERN.match(line):
                    funcname = match.group("funcname")
                    if self.funcnamefilter(funcname):
                        values.append(
                            SkippedFunction.from_parent(
                                name=funcname,
                                parent=self,
                                lineno=lineno,
                                reason=self.reason,
                            )
                        )

        return values


class SkippedFunction(pytest.Function):
    def __init__(
        self, name: str, parent: pytest.Collector, reason: str, lineno: int, **kwargs
    ):
        super().__init__(name, parent, **kwargs)
        self.reason = reason
        self.lineno = lineno

    def _getobj(self):
        return SkippedObj()

    def reportinfo(self) -> tuple[os.PathLike[str] | str, int | None, str]:
        return self.path, self.lineno, f"{self.name} [Skipped: {self.reason}]"

    def runtest(self):
        pytest.skip(reason=self.reason)


class SkippedObj:
    def __call__(self, *args, **kwargs):
        pass


def pytest_pycollect_makemodule(module_path: Path, parent: pytest.Collector):
    """Skip tests located in apps that are not installed in settings.INSTALLED_APPS.

    Tests files will be detected, but parsed without evaluation to avoid importing
    models from non-installed apps. Likewise, test functions within those files
    will be detected and reported as though decorated with @pytest.mark.skip."""
    for app_name in DISABLED_INTERNAL_APPS:
        if f"/{app_name}/" in module_path.as_posix():
            return SkippedModule.from_parent(
                parent=parent,
                path=module_path,
                reason=f"App '{app_name}' not found in settings.INSTALLED_APPS.",
            )
    return pytest.Module.from_parent(parent=parent, path=module_path)
