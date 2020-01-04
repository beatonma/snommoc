"""
To enable a module for testing:
- Add the module name to TEST_APPS in this file.
- Optionally, add custom settings to the file {app_name}.tests.config.test_settings
  - Any values here will be appended to, or replace, the default values
    found in basetest.test_settings_default

Very heavily inspired by : https://github.com/django/django/blob/master/tests/runtests.py
"""
import importlib
import sys
from typing import Dict

import colorama
import django
from django.apps import apps
from django.conf import settings
from django.test.utils import get_runner

# Not used here but needs to be initiated before nose runs (heh)
from basetest.args import RUNTESTS_CLARGS
from basetest.test_settings_default import *

TEST_APPS = [
    'api',
    'crawlers.parliamentdotuk',
    'crawlers.theyworkforyou',
    'dashboard',
    'notifications',
    'repository',
]


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

    except ModuleNotFoundError:
        pass

    settings.INSTALLED_APPS.append(app_name)

    # Ensure there are no duplicates
    settings.INSTALLED_APPS = list(set(settings.INSTALLED_APPS))

    print(f'INSTALLED_APPS: {settings.INSTALLED_APPS}')
    apps.set_installed_apps(settings.INSTALLED_APPS)

    test_runner = get_runner(settings)()
    test_results = test_runner.run_tests([f'{app_name}.tests'])

    _reset_settings(state)

    return test_results


def _reset_settings(state: Dict):
    for key, value in state.items():
        setattr(settings, key, value)


def _print_results(test_results):
    print()
    print(f'Django version: {django.get_version()}')
    print('Results:')
    colorama.init()
    for app, result in test_results.items():
        if result == 0:
            background_color = colorama.Back.RESET
            result_text = f'{colorama.Fore.GREEN}OK{colorama.Fore.RESET}'
        else:
            background_color = colorama.Back.RED
            result_text = f'{colorama.Style.BRIGHT}{colorama.Fore.WHITE}{result} '
        print(f'{colorama.Style.BRIGHT} {background_color} '
              f'{result_text.rjust(4)} {app} {colorama.Back.RESET} ')
    print()


def _main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'basetest.test_settings_default'

    django.setup()

    all_passed = True
    results = {}
    for module in TEST_APPS:
        failures = run_app_tests(module)
        results[module] = failures
        all_passed = all_passed and not bool(failures)

    _print_results(results)

    if not RUNTESTS_CLARGS.network:
        print(f'\n{colorama.Fore.CYAN}'
              'WARNING:\n  NetworkTestCase implementations were not executed!\n'
              '  Add `-network` flag to command line arguments when you want '
              'to run network tests.')
    sys.exit(all_passed)


if __name__ == '__main__':
    _main()
