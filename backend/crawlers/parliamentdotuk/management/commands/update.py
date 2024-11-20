import sys
from argparse import ArgumentParser
from typing import Callable

from crawlers.parliamentdotuk import tasks
from util.management.task_command import TaskCommand


class Command(TaskCommand):
    def add_arguments(self, parser: ArgumentParser):
        super().add_arguments(parser)
        command = parser.add_subparsers(dest="command")

        divisions = command.add_parser(
            "divisions",
            help="Update division data",
        ).add_subparsers(dest="scope")
        divisions.add_parser("commons", help="Update commons division data")
        divisions.add_parser("lords", help="Update lords division data")

        members = command.add_parser(
            "members",
            help="Update member data",
        ).add_subparsers(dest="scope")
        members.add_parser("active", help="Update detailed data for active members")
        members.add_parser("all", help="Update basic data for all members")
        members.add_parser("portraits", help="Update member portraits")

        constituencies = command.add_parser(
            "constituencies",
            help="Update constituency data, including boundaries and election results.",
        ).add_subparsers(dest="scope")
        constituencies.add_parser("", help="Update core constituency data")
        constituencies.add_parser("boundaries", help="Update geographical boundaries")
        constituencies.add_parser("elections", help="Update election results")

        bills = command.add_parser("bills", help="Update bill data")

    def handle(self, *args, command: str, **kwargs):
        func: Callable | None = None

        if command == "constituencies":
            func = self.handle_constituencies(**kwargs)
        elif command == "bills":
            func = tasks.update_bills
        elif command == "divisions":
            func = self.handle_divisions(**kwargs)
        elif command == "members":
            func = self.handle_members(**kwargs)

        if not func:
            self.print_help("manage.py", "update")
            sys.exit(1)

        self.handle_async(func, **kwargs)

    @staticmethod
    def handle_constituencies(scope: str, **kwargs) -> Callable:
        return {
            "elections": tasks.update_election_results,
            "boundaries": tasks.update_constituency_boundaries,
        }.get(scope, tasks.update_constituencies)

    @staticmethod
    def handle_divisions(scope: str, **kwargs) -> Callable:
        return {
            "commons": tasks.update_commons_divisions,
            "lords": tasks.update_lords_divisions,
        }.get(scope, None)

    @staticmethod
    def handle_members(scope: str, **kwargs) -> Callable:
        return {
            "active": tasks.update_active_member_details,
            "all": tasks.update_all_members_basic_info,
            "portraits": tasks.update_member_portraits,
        }.get(scope, tasks.update_active_member_details)
