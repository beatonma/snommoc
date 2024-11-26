import logging

from common.models import BaseQuerySet
from crawlers.context import TaskContext
from crawlers.wikipedia import wikipedia_client
from crawlers.wikipedia.tasks import schema
from repository.models import MemberPortrait, Person

log = logging.getLogger(__name__)


def update_wikipedia_member_portraits(
    members: BaseQuerySet[Person],
    context: TaskContext,
):
    members = members.filter(wikipedia__isnull=False)
    wiki_pages = members.values_list("wikipedia", flat=True)

    def get_images(name: str, data: schema.Images):
        member = members.get_or_none(wikipedia=name)
        if not member:
            log.warning(f"Failed to update images for member '{name}'")
            return

        _update_member_portrait(member, data, context)

    wikipedia_client.for_each_page(
        wiki_pages,
        get_images,
        page_class=schema.Images,
        context=context,
        prop="pageimages",
        piprop="original|thumbnail",
        pithumbsize=500,
    )


def _update_member_portrait(
    member: Person,
    images: schema.Images,
    context: TaskContext,
):
    defaults = {}
    if main := images.original:
        defaults["fullsize_url"] = main.source
    if thumbnail := images.thumbnail:
        defaults["square_url"] = thumbnail.source
        defaults["tall_url"] = thumbnail.source
        defaults["wide_url"] = thumbnail.source

    if defaults:
        MemberPortrait.objects.update_or_create(
            person=member,
            defaults=defaults,
        )
        context.info(f"Updated member portrait for {member}")
