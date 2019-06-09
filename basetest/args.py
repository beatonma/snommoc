import argparse
import sys


def _parse_args():
    def _consume_keys():
        """Remove our args from argv so they are not passed to nosetests."""
        keys = ['-network', ]
        for key in keys:
            if key in sys.argv:
                sys.argv.remove(key)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-network',
        action='store_true',
        default=False,
        help='Include network tests in the test suite')
    _args = parser.parse_args()

    _consume_keys()
    return _args


RUNTESTS_CLARGS = _parse_args()
