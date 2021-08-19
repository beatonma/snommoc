import logging

from django.db.models import QuerySet

from crawlers.wikipedia import wikipedia_client
from repository.models import MemberPortrait, Person

log = logging.getLogger(__name__)


def _get_wikipedia_images(members: QuerySet[Person]) -> dict:
    """
    :returns dictionary with the format:
        {
            "name": {
                "main": "url",
                "thumbnail": "url"
            }
        }
    """
    member_images_map = {}
    wiki_pages = [m.wikipedia for m in members if m.wikipedia]

    def get_main_image(name, data):
        if "original" in data:
            m = member_images_map.get(name, {})
            m["main"] = data["original"].get("source")
            member_images_map[name] = m

    def get_thumbnail(name, data):
        if "thumbnail" in data:
            m = member_images_map.get(name, {})
            m["thumbnail"] = data["thumbnail"].get("source")
            member_images_map[name] = m

    wikipedia_client.for_each_page(
        wiki_pages,
        get_main_image,
        prop="pageimages",
        piprop="original",
    )

    wikipedia_client.for_each_page(
        wiki_pages,
        get_thumbnail,
        prop="pageimages",
        pithumbsize=1000,
    )

    return member_images_map


def _update_member_portrait(member: Person, images: dict):
    if not images:
        # if images.main is None and images.thumbnail is None:
        log.warning(f"No Wikipedia images for member {member}")
        return

    main = images.get("main")
    thumbnail = images.get("thumbnail")

    try:
        MemberPortrait.objects.update_or_create(
            person=member,
            defaults={
                "fullsize_url": main,
                "square_url": thumbnail,
                "tall_url": thumbnail,
                "wide_url": thumbnail,
            },
        )
    except Exception:
        log.warning(
            f"Failed to update MemberPortrait for member={member} with images={images}"
        )


def update_wikipedia_member_portraits(members: QuerySet[Person]):
    """
    Sample url:
    https://en.wikipedia.org/w/api.php?action=query&titles=Dawn_Butler&prop=pageimages&piprop=original&format=json&pilicense=free
    """
    log.debug(f"Looking for portraits for {members.count()} members...")

    member_images = _get_wikipedia_images(members)

    for p in members:
        images_for_member = member_images.get(p.wikipedia)
        _update_member_portrait(p, images_for_member)
