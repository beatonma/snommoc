import argparse
import sys


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-network',
        action='store_true',
        default=False,
        help='Include network tests in the test suite')

    parser.add_argument(
        '--app',
        type=str,
        help='Only run tests for a specific app',
        default=None,
    )

    _args, remaining = parser.parse_known_args()
    sys.argv = remaining

    return _args


RUNTESTS_CLARGS = _parse_args()
