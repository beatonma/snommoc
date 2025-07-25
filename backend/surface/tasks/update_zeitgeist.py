import logging
from datetime import date
from typing import Type

from celery import shared_task
from common.cache import invalidate_cache
from common.models import BaseModel
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from notifications.models.task_notification import task_notification
from repository.models import Bill, CommonsDivision, LordsDivision, Person
from social.models import Comment, Vote
from surface import cache
from surface.models import (
    FeaturedBill,
    FeaturedCommonsDivision,
    FeaturedLordsDivision,
    FeaturedPerson,
)
from surface.models.featured import BaseFeatured
from surface.models.zeitgeist import ZeitgeistItem
from util.time import coerce_timezone, get_today

log = logging.getLogger(__name__)

RECENT_ENGAGEMENT_SAMPLE_SIZE = 20

ZEITGEIST_TARGET_MODELS = [
    Person,
    Bill,
    CommonsDivision,
    LordsDivision,
]

# Try to ensure there are least this many ZeitgeistItem instances for each of the target models.
TARGET_COUNT_PER_TYPE = 5


@shared_task
@task_notification(label="Update zeitgeist", level=logging.DEBUG)
def update_zeitgeist(**kwargs):
    _reset_zeitgeist()
    today = get_today()

    _update_from_featured(today)
    _update_from_social()
    _update_from_recent(today)

    invalidate_cache(cache.API_VIEW_CACHE)


def _update_from_featured(today: date):
    _update_featured_people(today)
    _update_featured_commons_divisions(today)
    _update_featured_lords_divisions(today)
    _update_featured_bills(today)


def _update_from_social():
    for model in ZEITGEIST_TARGET_MODELS:
        ct = ContentType.objects.get_for_model(model)
        comments = _filter_social_content(Comment, ct)
        votes = _filter_social_content(Vote, ct)

        for created_at, _id in comments + votes:
            ZeitgeistItem.objects.update_or_create(
                target_id=_id,
                target_type=ct,
                defaults={
                    "reason": ZeitgeistItem.Reason.SOCIAL,
                    "created_at": coerce_timezone(created_at),
                },
            )


def _update_from_recent(today: date):
    """Generate items from recent updates if featured + social don't result in enough data."""
    for model in ZEITGEIST_TARGET_MODELS:
        ct = ContentType.objects.get_for_model(model)
        existing_count = ZeitgeistItem.objects.filter(target_type=ct).count()

        try_to_make_n = TARGET_COUNT_PER_TYPE - existing_count
        created_count = 0

        qs = model.objects.order_by("-created_at")
        for item in qs:
            obj, created = ZeitgeistItem.objects.get_or_create(
                target_type=ct,
                target_id=item.pk,
                defaults={
                    "reason": ZeitgeistItem.Reason.DEFAULT,
                    "created_at": coerce_timezone(today),
                },
            )
            if created:
                log.info(f"Created {obj}")
                created_count += 1
            if created_count >= try_to_make_n:
                break


def _reset_zeitgeist():
    ZeitgeistItem.objects.all().delete()


def _filter_social_content(model: Type[BaseModel], content_type: ContentType) -> list:
    return list(
        model.objects.filter(
            target_type=content_type,
        )
        .order_by(
            "created_at",
        )
        .values_list(
            "created_at",
            "target_id",
        )[:RECENT_ENGAGEMENT_SAMPLE_SIZE]
    )


def _filter_featured_content(model: Type[BaseFeatured], today: date):
    return (
        model.objects.filter(Q(start__isnull=True) | Q(start__lte=today))
        .filter(Q(end__isnull=True) | Q(end__gte=today))
        .select_related("target")
    )


def _update_featured_people(today: date):
    for x in _filter_featured_content(FeaturedPerson, today):
        _create_featured_zeitgeist_item(Person, x.start or today, x.target.pk)


def _update_featured_commons_divisions(today: date):
    for x in _filter_featured_content(FeaturedCommonsDivision, today):
        _create_featured_zeitgeist_item(
            CommonsDivision,
            x.start or today,
            x.target.pk,
        )


def _update_featured_lords_divisions(today: date):
    for x in _filter_featured_content(FeaturedLordsDivision, today):
        _create_featured_zeitgeist_item(LordsDivision, x.start or today, x.target.pk)


def _update_featured_bills(today: date):
    for x in _filter_featured_content(FeaturedBill, today):
        _create_featured_zeitgeist_item(Bill, x.start or today, x.target.pk)


def _create_featured_zeitgeist_item(model, created_at: date, _id):
    ct = ContentType.objects.get_for_model(model)
    ZeitgeistItem.objects.update_or_create(
        target_id=_id,
        target_type=ct,
        defaults={
            "reason": ZeitgeistItem.Reason.FEATURE,
            "created_at": coerce_timezone(created_at),
        },
    )
