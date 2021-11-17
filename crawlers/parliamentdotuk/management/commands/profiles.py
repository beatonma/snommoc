from crawlers.parliamentdotuk.tasks import (
    update_profiles_for_active_members,
    update_profiles_for_all_members,
)
from crawlers.parliamentdotuk.tasks.membersdataplatform.active_members import (
    update_details_for_member,
)
from util.management.async_command import AsyncCommand


class Command(AsyncCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            "-all",
            action="store_true",
            default=False,
            help="Update profile details for active and historic members.",
        )

        parser.add_argument(
            "--member_id", type=int, help="Update all details for a single person."
        )

    def handle(self, *args, **command_options):
        kwargs = None

        if command_options["member_id"]:
            func = update_details_for_member
            kwargs = {"member_id": command_options["member_id"]}

        elif command_options["all"]:
            func = update_profiles_for_all_members

        else:
            func = update_profiles_for_active_members

        self.handle_async(func, func_kwargs=kwargs, **command_options)
