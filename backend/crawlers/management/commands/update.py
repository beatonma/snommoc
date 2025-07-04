import sys
from typing import Callable

from crawlers import tasks as multi_source
from crawlers.parliamentdotuk import tasks as parliament
from django.core.management import CommandParser
from util.management.task_command import TaskCommand


class Command(TaskCommand):
    def add_arguments(self, parser: CommandParser):
        super().add_arguments(parser)
        command = parser.add_subparsers(dest="command")

        command.add_parser("bills", help="Update bill data")

        constituencies = command.add_parser(
            "constituencies",
            help="Update constituency data, including boundaries and election results.",
        ).add_subparsers(dest="scope")
        constituencies.add_parser("boundaries", help="Update geographical boundaries")
        constituencies.add_parser("elections", help="Update election results")

        command.add_parser(
            "demographics", help="Update current demographics data of Lords and MPs"
        )

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
        members.add_parser("portraits", help="Update member portraits")

    def handle(self, *args, command: str, **kwargs):
        func: Callable | None = None

        if command == "bills":
            func = parliament.update_bills
        elif command == "constituencies":
            func = self.handle_constituencies(**kwargs)
        elif command == "demographics":
            func = parliament.update_demographics
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
            "elections": parliament.update_election_results,
            "boundaries": parliament.update_constituency_boundaries,
        }.get(scope, parliament.update_constituencies)

    @staticmethod
    def handle_divisions(scope: str, **kwargs) -> Callable:
        return {
            "commons": parliament.update_commons_divisions,
            "lords": parliament.update_lords_divisions,
        }.get(scope, None)

    @staticmethod
    def handle_members(scope: str, **kwargs) -> Callable:
        return {
            "active": parliament.update_members,
            "portraits": multi_source.update_member_portraits,
        }.get(scope, parliament.update_members)
