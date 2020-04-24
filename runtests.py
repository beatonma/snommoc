"""
To enable a module for testing:
- Add the module name to TEST_APPS in this file.
- Optionally, add custom settings to the file {app_name}.tests.config.test_settings
  - Any values here will be appended to, or replace, the default values
    found in basetest.test_settings_default

Very heavily inspired by : https://github.com/django/django/blob/master/tests/runtests.py
"""
import argparse
import datetime
import importlib
import json
import re
import sys
from typing import (
    Dict,
)
from unittest import TextTestResult

import colorama
import django
from django.apps import apps
from django.conf import settings
# Not used here but needs to be initiated before nose runs (heh)
from django_nose import BasicNoseRunner

from basetest.args import RUNTESTS_CLARGS
from basetest.test_settings_default import *

TEST_METHOD_REGEX = re.compile(r'(test_[^\s]+)')
ERROR_REGEX = re.compile(r'.*\n([^\n]+)', re.DOTALL)
ASSERTION_REGEX = re.compile(r'.*(line [\d]+).*AssertionError: (.*?)\n', re.DOTALL)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_HISTORY_FILE = os.path.join(BASE_DIR, '.runtests.json')


TEST_APPS = [
    'api',
    'crawlers.parliamentdotuk',
    'crawlers.theyworkforyou',
    'dashboard',
    'notifications',
    'repository',
    'util',
]


def _highlight_foreground(text, color):
    return f'{color}{text}{colorama.Fore.RESET}'


def _highlight_good(text):
    return _highlight_foreground(text, colorama.Fore.LIGHTGREEN_EX)


def _highlight_bad(text):
    return _highlight_foreground(text, colorama.Fore.BLUE)


def _highlight_warning(text):
    return _highlight_foreground(text, colorama.Fore.CYAN)


def _get_test_method_name(test):
    try:
        return re.match(
            TEST_METHOD_REGEX,
            test.__str__()
        ).group(1)
    except Exception:
        return 'runTest'


class VerboseResult:

    def __init__(self, result: TextTestResult):
        self.tests_run = result.testsRun
        not_implemented_errors = [x for x in result.errors if 'NotImplementedError' in x.__str__()]
        self.not_implemented = [_get_test_method_name(x[0]) for x in not_implemented_errors]
        self.errors = [VerboseError(x) for x in result.errors if x not in not_implemented_errors]
        self.failures = [VerboseFailure(x) for x in result.failures]
        self.successful = result.testsRun - len(result.errors) - len(result.failures)

    def passed(self) -> bool:
        return self.successful == self.tests_run

    def report(self, app_name) -> str:

        def report_all_passed(indent=2):
            return f'{" " * indent}{_highlight_good("OK")}  [{_highlight_good(self.successful) if self.successful else _highlight_warning(self.successful)}] {app_name}'

        def report_success(indent=2):
            if not self.successful:
                return ''
            return f'{" " * indent}{_highlight_good(str(self.successful)).rjust(2)} passed\n'

        def report_errors(indent=2):
            if not self.errors:
                return ''
            return f'{" " * indent}{_highlight_bad(str(len(self.errors)).rjust(2))} errors:\n' + \
                   '\n'.join([f'{" " * indent * 3}{x.report()}' for x in self.errors]) + \
                   '\n'

        def report_not_implemented(indent=2):
            if not self.not_implemented:
                return ''
            return f'{" " * indent}{_highlight_warning(str(len(self.not_implemented)).rjust(2))} not implemented:\n' + \
                   '\n'.join([f'{" " * indent * 3}{x}' for x in self.not_implemented]) + \
                   '\n'

        def report_failures(indent=2):
            if not self.failures:
                return ''
            return f'{" " * indent}{_highlight_bad(str(len(self.failures)).rjust(2))} failures:\n' + \
                   '\n'.join([f'{" " * indent * 3}{x.report()}' for x in self.failures])

        if self.passed():
            return report_all_passed(indent=2)
            # return f'  {_highlight_good("OK")}  [{_highlight_good(self.successful)}] {app_name}'
        else:
            return (
                '\n'
                f'! {_highlight_bad(app_name)}:\n'
                f'  {self.tests_run} test ran\n'
                f'{report_success(indent=2)}'
                f'{report_not_implemented(indent=2)}'
                f'{report_errors(indent=2)}'
                f'{report_failures(indent=2)}'
            )


class VerboseError:
    def __init__(self, error):
        _testcase, _message = error
        self.test_method_name = _get_test_method_name(_testcase)
        self.exception = re.match(ERROR_REGEX, _message).group(1)

    def report(self) -> str:
        return f'{self.test_method_name}: {self.exception}'


class VerboseFailure:
    def __init__(self, failure):
        _testcase, _message = failure
        self.test_method_name = _get_test_method_name(_testcase)
        assertion_matches = re.match(
            ASSERTION_REGEX,
            _message
        )
        self.line = assertion_matches.group(1)
        self.failed_assertion = assertion_matches.group(2)

    def report(self) -> str:
        return f'{self.test_method_name} [{self.line}]: {self.failed_assertion}'


class VerboseTestRunner(BasicNoseRunner):

    def suite_result(self, suite, result, **kwargs):
        # Overrides BasicNoseRunner.suite_result
        return self.verbose_suite_result(suite, result, **kwargs)

    def verbose_suite_result(self, suite, result: TextTestResult, **kwargs):
        return VerboseResult(result)


def run_app_tests(app_name):
    print(f'Running tests for app `{app_name}`')
    state = {
        'INSTALLED_APPS': [*settings.INSTALLED_APPS],
        'ROOT_URLCONF': getattr(settings, 'ROOT_URLCONF', ''),
        'TEMPLATES': settings.TEMPLATES,
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'STATIC_URL': settings.STATIC_URL,
        'STATIC_ROOT': settings.STATIC_ROOT,
        'MIDDLEWARE': settings.MIDDLEWARE,
    }

    try:
        # Check if this app defines a custom settings configuration.
        settings_path = f'{app_name}.tests.config.test_settings'
        if importlib.util.find_spec(settings_path):
            app_settings = importlib.import_module(settings_path)
            if hasattr(app_settings, 'INSTALLED_APPS'):
                settings.INSTALLED_APPS += [*app_settings.INSTALLED_APPS]
            if hasattr(app_settings, 'ROOT_URLCONF'):
                settings.ROOT_URLCONF = app_settings.ROOT_URLCONF
            if hasattr(app_settings, 'MIDDLEWARE'):
                settings.MIDDLEWARE = app_settings.MIDDLEWARE

    except ModuleNotFoundError:
        pass

    settings.INSTALLED_APPS.append(app_name)

    # Ensure there are no duplicates
    settings.INSTALLED_APPS = list(set(settings.INSTALLED_APPS))

    print(f'INSTALLED_APPS: {settings.INSTALLED_APPS}')
    apps.set_installed_apps(settings.INSTALLED_APPS)

    test_runner = VerboseTestRunner()
    test_results = test_runner.run_tests([f'{app_name}.tests'])

    _reset_settings(state)

    return test_results


def _reset_settings(state: Dict):
    for key, value in state.items():
        setattr(settings, key, value)


def _compare_tests_with_previous(tests_run: int):
    def _save_current():
        with open(TEST_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'tests_run': tests_run,
                'timestamp': datetime.datetime.now().strftime('%y-%m-%d'),
            }, f)

    def _load_previous() -> int:
        previous_run = {}
        if os.path.exists(TEST_HISTORY_FILE):
            with open(TEST_HISTORY_FILE, 'r', encoding='utf-8') as f:
                previous_run = json.load(f)

        return previous_run.get('tests_run', 0)

    previous_tests_run = _load_previous()
    if previous_tests_run > tests_run:
        print(_highlight_warning(f'Previous run had {previous_tests_run} tests (vs {tests_run} now). Is everything okay?'))
    else:
        _save_current()


def _print_results(test_results: Dict[str, VerboseResult], tests_passed: int, tests_run: int):
    print()
    print(f'Django version: {django.get_version()}')
    print('Results:')
    colorama.init()
    ordered_apps = sorted(test_results.keys(), key=lambda x: not test_results[x].passed())
    for app in ordered_apps:
        result = test_results.get(app)
        print(result.report(app_name=app))
    print()
    if tests_passed == tests_run:
        print(_highlight_good(f'All {tests_run} tests passed'))
    else:
        print(_highlight_warning(f'{tests_passed}/{tests_run} tests passed'))

    _compare_tests_with_previous(tests_run)


# def _parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         '--app',
#         type=str,
#         help='Only run tests for a specific app',
#         default=None,
#     )
#
#     args, remaining_args = parser.parse_known_args()
#     sys.argv = remaining_args
#     return args


def _main():
    global TEST_APPS

    if RUNTESTS_CLARGS.app is not None and RUNTESTS_CLARGS.app in TEST_APPS:
        print(_highlight_warning(f'Only running tests for app={RUNTESTS_CLARGS.app}'))
        TEST_APPS = [RUNTESTS_CLARGS.app]

    os.environ['DJANGO_SETTINGS_MODULE'] = 'basetest.test_settings_default'

    django.setup()

    all_passed = True
    tests_run = 0
    tests_passed = 0
    app_results = {}
    for module in TEST_APPS:
        results = run_app_tests(module)
        app_results[module] = results
        all_passed = all_passed and results.passed()
        tests_run += results.tests_run
        tests_passed += results.successful

    _print_results(app_results, tests_passed=tests_passed, tests_run=tests_run)

    if not RUNTESTS_CLARGS.network:
        print(_highlight_warning(
            '\n'
            'WARNING:\n  NetworkTestCase implementations were not executed!\n'
            '  Add `-network` flag to command line arguments when you want '
            'to run network tests.'))
    if RUNTESTS_CLARGS.app is not None:
        print(_highlight_warning(f'Only ran tests for app={RUNTESTS_CLARGS.app}'))

    sys.exit(not all_passed)  # Return 0 if everything okay, 1 if failures


if __name__ == '__main__':
    _main()
