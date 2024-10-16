"""
Update member portrait urls
"""
from crawlers.parliamentdotuk.tasks import (
    update_member_portraits,
    update_missing_member_portraits_wikipedia,
)
from crawlers.parliamentdotuk.tasks.membersdataplatform.member_portrait import (
    update_member_portrait,
)
from repository.models import MemberPortrait, Person
from repository.resolution.members import get_member_by_name, normalize_name
from util.management.async_command import AsyncCommand


class Command(AsyncCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            "-wiki",
            action="store_true",
            default=False,
            help="Use confirmed wikipedia pages to find missing portraits.",
        )

        parser.add_argument(
            "--id",
            type=int,
            default=None,
            help="Update the portrait for a single member by parliamentdotuk ID.",
        )

        parser.add_argument(
            "--name",
            type=str,
            default=None,
            help="Update the portrait for a single member by name.",
        )

    def handle(self, *args, **options):
        id = options.get("id")
        name = options.get("name")

        if id or name:
            _update_single_member(
                id=id,
                name=name,
            )
            return

        if options.get("wiki"):
            func = update_missing_member_portraits_wikipedia
        else:
            func = update_member_portraits

        self.handle_async(func, *args, **options)


def _update_single_member(id: int = None, name: str = None):
    if id:
        member = Person.objects.get(pk=id)
    else:
        member = get_member_by_name(normalize_name(name))

    if member is None:
        raise Exception(f"Member not found: name={name} [id={id}]")

    print(f"Trying to update portrait for member {member}")
    update_member_portrait(member)

    try:
        print(f"Portrait: {MemberPortrait.objects.get(person=member)}")
    except MemberPortrait.DoesNotExist:
        print(f"Unable to find portrait for member {member}")
