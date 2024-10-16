"""
This is a scratch file for running some command to help with debugging. It is not for long term use.
"""
from crawlers.network import json_cache
from crawlers.parliamentdotuk.tasks.lda.update_election_results import (
    fetch_and_create_election_result,
)
from util.management.async_command import AsyncCommand


class Command(AsyncCommand):
    def handle(self, *args, **options):
        # find_keir_starmer_election_results()
        self.handle_async(debug, *args, **options)


@json_cache(name="debug")
def find_caroline_lucas_election_results(**kwargs):
    constituency_result_ids = [382667, 382668, 730287, 1223142]

    for pk in constituency_result_ids:
        fetch_and_create_election_result(pk, cache=kwargs.get("cache"))


@json_cache(name="debug")
def find_boris_johnson_election_results(**kwargs):
    constituency_result_ids = [383586, 730738, 1223593]

    for pk in constituency_result_ids:
        fetch_and_create_election_result(pk, cache=kwargs.get("cache"))


@json_cache(name="debug")
def find_keir_starmer_election_results(**kwargs):
    constituency_result_ids = [383015, 730457, 1223312]

    for pk in constituency_result_ids:
        fetch_and_create_election_result(pk, cache=kwargs.get("cache"))


def debug(*args, **kwargs):
    print(f"debug({args}, {kwargs})")
