"""
To enable a module for testing:
- Create a Django settings file called test_settings.py in {appname}/tests//config/
- Add the module name to TEST_APPS in this file.
"""
import sys
from importlib.util import find_spec

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
    'repository',
    'crawlers.parliamentdotuk',
    'crawlers.theyworkforyou',
]


def run_app_tests(app_name):
    settings_path = f'{app_name}.tests.config.test_settings'
    try:
        # Load settings from module if the module has its own settings file
        if find_spec(settings_path):
            print(f'Using app settings file {settings_path}')
            os.environ['DJANGO_SETTINGS_MODULE'] = settings_path
    except ModuleNotFoundError:
        print(f'App \'{app_name}\' is using the default test settings')

    _reset_settings()

    if app_name not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS.append(app_name)

    django.setup()
    apps.set_installed_apps(settings.INSTALLED_APPS)

    test_runner = get_runner(settings)()
    test_results = test_runner.run_tests([f'{app_name}.tests'])
    return test_results


def _reset_settings():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'defaulttestconfig.test_settings_default')
    settings.ALLOWED_HOSTS = ALLOWED_HOSTS
    settings.INSTALLED_APPS = INSTALLED_APPS
    settings.MIDDLEWARE = MIDDLEWARE
    settings.DATABASES = DATABASES
    settings.SECRET_KEY = SECRET_KEY
    settings.LANGUAGE_CODE = LANGUAGE_CODE
    settings.TEST_RUNNER = TEST_RUNNER
    settings.NOSE_ARGS = NOSE_ARGS


def _print_results(test_results):
    print()
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
