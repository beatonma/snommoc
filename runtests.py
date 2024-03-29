#! env/bin/python
"""
To enable a module for testing:
- Add the module name to TEST_APPS in this file.
- Optionally, add custom settings to the file {app_name}.tests.config.test_settings
  - Any values here will be appended to, or replace, the default values
    found in basetest.test_settings_default

Very heavily inspired by : https://github.com/django/django/blob/master/tests/runtests.py
"""
import datetime
import importlib
import json
import random
import re
import sys
from typing import Dict
from unittest import TestCase, TextTestResult

import colorama
import django
from django.apps import apps
from django.conf import settings

# Not used here but needs to be initiated before nose runs (heh)
from django_nose import BasicNoseRunner

from basetest.args import RUNTESTS_CLARGS
from basetest.test_settings_default import *
from basetest.testcase import LocalTestCalledNetwork
from util.time import get_now

TEST_METHOD_REGEX = re.compile(r"(test_[^\s]+)")
ERROR_REGEX = re.compile(r".*\n([^\n]+)", re.DOTALL)
ASSERTION_REGEX = re.compile(r".*(line [\d]+).*AssertionError: (.*?)\n", re.DOTALL)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_HISTORY_FILE = os.path.join(BASE_DIR, ".runtests.json")


TEST_APPS = [
    "basetest",
    "api",
    "crawlers.network",
    "crawlers.parliamentdotuk",
    "crawlers.wikipedia",
    "dashboard",
    "notifications",
    "repository",
    "social",
    "surface",
    "util",
]
random.shuffle(TEST_APPS)


def _highlight_foreground(text, color):
    return f"{color}{text}{colorama.Fore.RESET}"


def _highlight_good(text):
    return _highlight_foreground(text, colorama.Fore.LIGHTGREEN_EX)


def _highlight_bad(text):
    return _highlight_foreground(text, colorama.Fore.BLUE)


def _highlight_warning(text):
    return _highlight_foreground(text, colorama.Fore.CYAN)


def _print_good(text):
    print(_highlight_good(text))


def _print_warning(text):
    print(_highlight_warning(text))


def _get_test_method_name(test: TestCase):
    try:
        return re.match(TEST_METHOD_REGEX, test.__str__()).group(1)
    except Exception as e:
        _print_warning(f"Cannot parse method name: test={test} ({e})")
        return f"{test}"


class VerboseResult:
    def __init__(self, result: TextTestResult):
        self.tests_run = result.testsRun
        not_implemented_errors = [
            x for x in result.errors if "NotImplementedError" in x.__str__()
        ]
        self.not_implemented = [
            _get_test_method_name(x[0]) for x in not_implemented_errors
        ]
        self.errors = [
            VerboseError(x) for x in result.errors if x not in not_implemented_errors
        ]
        self.failures = [VerboseFailure(x) for x in result.failures]
        self.successful = result.testsRun - len(result.errors) - len(result.failures)

    def passed(self) -> bool:
        return self.successful == self.tests_run

    def report(self, app_name) -> str:
        def report_all_passed(indent=2):
            return (
                f'{" " * indent}{_highlight_good("OK")} '
                f" [{_highlight_good(self.successful) if self.successful else _highlight_warning(self.successful)}]"
                f" {app_name}"
            )

        def report_success(indent=2):
            if not self.successful:
                return ""
            return (
                f'{" " * indent}{_highlight_good(str(self.successful)).rjust(2)}'
                " passed\n"
            )

        def report_errors(indent=2):
            if not self.errors:
                return ""
            return (
                f'{" " * indent}{_highlight_bad(str(len(self.errors)).rjust(2))}'
                " errors:\n"
                + "\n".join([f'{" " * indent * 3}{x.report()}' for x in self.errors])
                + "\n"
            )

        def report_not_implemented(indent=2):
            if not self.not_implemented:
                return ""
            return (
                f'{" " * indent}{_highlight_warning(str(len(self.not_implemented)).rjust(2))}'
                " not implemented:\n"
                + "\n".join([f'{" " * indent * 3}{x}' for x in self.not_implemented])
                + "\n"
            )

        def report_failures(indent=2):
            if not self.failures:
                return ""
            return (
                f'{" " * indent}{_highlight_bad(str(len(self.failures)).rjust(2))}'
                " failures:\n"
                + "\n".join([f'{" " * indent * 3}{x.report()}' for x in self.failures])
            )

        if self.passed():
            return report_all_passed(indent=2)
        else:
            return (
                "\n"
                f"! {_highlight_bad(app_name)}:\n"
                f"  {self.tests_run} test ran\n"
                f"{report_success(indent=2)}"
                f"{report_not_implemented(indent=2)}"
                f"{report_errors(indent=2)}"
                f"{report_failures(indent=2)}"
            )


class VerboseError:
    def __init__(self, error):
        _testcase, _message = error
        self.test_method_name = _get_test_method_name(_testcase)
        self.exception = re.match(ERROR_REGEX, _message).group(1)

    def report(self) -> str:
        return f"{self.test_method_name}: {self.exception}"


class VerboseFailure:
    def __init__(self, failure):
        _testcase, _message = failure
        self.test_method_name = _get_test_method_name(_testcase)
        assertion_matches = re.match(ASSERTION_REGEX, _message)
        self.line = assertion_matches.group(1)
        self.failed_assertion = assertion_matches.group(2)

    def report(self) -> str:
        return f"{self.test_method_name} [{self.line}]: {self.failed_assertion}"


class VerboseTestRunner(BasicNoseRunner):
    def suite_result(self, suite, result, **kwargs):
        # Overrides BasicNoseRunner.suite_result
        return self.verbose_suite_result(suite, result, **kwargs)

    def verbose_suite_result(self, suite, result: TextTestResult, **kwargs):
        return VerboseResult(result)


def run_app_tests(app_name):
    print(f"Running tests for app `{app_name}`")
    state = {
        "INSTALLED_APPS": [*settings.INSTALLED_APPS],
        "ROOT_URLCONF": getattr(settings, "ROOT_URLCONF", ""),
        "TEMPLATES": settings.TEMPLATES,
        "LANGUAGE_CODE": settings.LANGUAGE_CODE,
        "STATIC_URL": settings.STATIC_URL,
        "STATIC_ROOT": settings.STATIC_ROOT,
        "MIDDLEWARE": settings.MIDDLEWARE,
    }

    try:
        # Check if this app defines a custom settings configuration.
        settings_path = f"{app_name}.tests.config.test_settings"
        if importlib.util.find_spec(settings_path):
            app_settings = importlib.import_module(settings_path)
            if hasattr(app_settings, "INSTALLED_APPS"):
                settings.INSTALLED_APPS += [*app_settings.INSTALLED_APPS]
            if hasattr(app_settings, "ROOT_URLCONF"):
                settings.ROOT_URLCONF = app_settings.ROOT_URLCONF
            if hasattr(app_settings, "MIDDLEWARE"):
                settings.MIDDLEWARE = app_settings.MIDDLEWARE

    except ModuleNotFoundError:
        pass

    settings.INSTALLED_APPS.append(app_name)

    # Ensure there are no duplicates
    settings.INSTALLED_APPS = list(set(settings.INSTALLED_APPS))

    print(f"INSTALLED_APPS: {settings.INSTALLED_APPS}")
    apps.set_installed_apps(settings.INSTALLED_APPS)

    test_runner = VerboseTestRunner()
    test_results = test_runner.run_tests([f"{app_name}.tests"])

    from django.contrib.contenttypes.models import ContentType

    ContentType.objects.clear_cache()

    _reset_settings(state)
    apps.unset_installed_apps()

    return test_results


def _reset_settings(state: Dict):
    for key, value in state.items():
        setattr(settings, key, value)


def _compare_tests_with_previous(tests_run: int):
    def _save_current():
        with open(TEST_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "tests_run": tests_run,
                    "timestamp": get_now().strftime("%y-%m-%d"),
                },
                f,
            )

    def _load_previous() -> int:
        previous_run = {}
        if os.path.exists(TEST_HISTORY_FILE):
            with open(TEST_HISTORY_FILE, "r", encoding="utf-8") as f:
                previous_run = json.load(f)

        return previous_run.get("tests_run", 0)

    previous_tests_run = _load_previous()
    if previous_tests_run > tests_run:
        _print_warning(
            f"Previous run had {previous_tests_run} tests (vs {tests_run} now). Is"
            " everything okay?"
        )
    else:
        _save_current()


def _print_results(
    test_results: Dict[str, VerboseResult],
    all_passed: bool,
    tests_passed: int,
    tests_run: int,
    repetitions: int,
    time_started: datetime.datetime,
    time_finished: datetime.datetime,
):
    print()
    print(f"Django version: {django.get_version()}")
    print(f"Modules tested: {TEST_APPS}")
    print()
    print("Results:")
    colorama.init()
    ordered_apps = sorted(
        test_results.keys(), key=lambda x: not test_results[x].passed()
    )

    for app in ordered_apps:
        result = test_results.get(app)
        print(result.report(app_name=app))

    print()
    repetitions_text = "" if repetitions <= 1 else f" [{repetitions} repeats]"

    if all_passed:
        _print_good(f"All {tests_run} tests passed{repetitions_text}")
    else:
        _print_warning(f"{tests_passed}/{tests_run} tests passed{repetitions_text}")

    print(
        f"Finished at {time_finished.strftime('%H:%M:%S')} [duration:"
        f" {time_finished - time_started}]"
    )

    _compare_tests_with_previous(tests_run)


def _catch_network_call(*args, **kwargs):
    raise LocalTestCalledNetwork(f"Illegal network call: {args} [{kwargs}]")


def _main():
    global TEST_APPS

    time_started = datetime.datetime.now()

    if RUNTESTS_CLARGS.app is not None and RUNTESTS_CLARGS.app in TEST_APPS:
        _print_warning(f"Only running tests for app={RUNTESTS_CLARGS.app}")
        TEST_APPS = [RUNTESTS_CLARGS.app]

    os.environ["DJANGO_SETTINGS_MODULE"] = "basetest.test_settings_default"

    django.setup()

    if not RUNTESTS_CLARGS.network:
        import crawlers.network

        crawlers.network.get_json = lambda *args, **kwargs: _catch_network_call(
            *args, **kwargs
        )

    all_passed = True
    tests_run = 0
    tests_passed = 0
    app_results = {}

    for module in TEST_APPS:
        fragile_broken = False
        for n in range(RUNTESTS_CLARGS.repeat):
            results = run_app_tests(module)
            passed = results.passed()
            failed = not passed

            if n == 0 or failed:
                app_results[module] = results
                all_passed = all_passed and passed
                tests_run += results.tests_run
                tests_passed += results.successful

            if failed:
                if RUNTESTS_CLARGS.repeat > 1:
                    _print_warning(f"FAILED on repetition {n}")

                if RUNTESTS_CLARGS.fragile:
                    _print_warning(
                        f"[FRAGILE] Module '{module}' has errors - exiting early!"
                    )
                    fragile_broken = True
                    break

        if fragile_broken:
            break

    time_finished = datetime.datetime.now()

    _print_results(
        app_results,
        all_passed=all_passed,
        tests_passed=tests_passed,
        tests_run=tests_run,
        repetitions=RUNTESTS_CLARGS.repeat,
        time_started=time_started,
        time_finished=time_finished,
    )

    if not RUNTESTS_CLARGS.network:
        _print_warning(
            "\n"
            "WARNING:\n  NetworkTestCase implementations were not executed!\n"
            "  Add `-network` flag to command line arguments when you want "
            "to run network tests."
        )
    if RUNTESTS_CLARGS.app is not None:
        _print_warning(f"Only ran tests for app={RUNTESTS_CLARGS.app}")

    sys.exit(not all_passed)  # Return 0 if everything okay, 1 if failures


if __name__ == "__main__":
    _main()
