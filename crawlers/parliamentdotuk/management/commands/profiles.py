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

    def handle(self, *args, **options):
        kwargs = None

        if options["member_id"]:
            func = update_details_for_member
            kwargs = {"member_id": options["member_id"]}

        elif options["all"]:
            func = update_profiles_for_all_members

        else:
            func = update_profiles_for_active_members

        self.handle_async(func, *args, kwargs=kwargs, **options)
