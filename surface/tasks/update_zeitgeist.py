"""

"""
import datetime
import logging
from typing import Type

from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from notifications.models.task_notification import TaskNotification, task_notification
from repository.models import (
    Bill,
    CommonsDivision,
    LordsDivision,
    Person,
)
from repository.models.mixins import BaseModel
from social.models import (
    Comment,
    Vote,
)
from surface.models import FeaturedPerson
from surface.models.featured import (
    BaseFeatured,
    FeaturedBill,
    FeaturedCommonsDivision,
    FeaturedLordsDivision,
)
from surface.models.zeitgeist import ZeitgeistItem
from util.time import get_today, coerce_timezone

log = logging.getLogger(__name__)


RECENT_ENGAGEMENT_SAMPLE_SIZE = 20


ZEITGEIST_TARGET_MODELS = [
    Person,
    Bill,
    CommonsDivision,
    LordsDivision,
]


@shared_task
@task_notification(label="Update zeitgeist", level=TaskNotification.LEVEL_DEBUG)
def update_zeitgeist(**kwargs):
    _reset_zeitgeist()

    _update_from_featured()
    _update_from_social()


def _update_from_featured():
    today = get_today()

    _update_featured_people(today)
    _update_featured_commons_divisions(today)
    _update_featured_lords_divisions(today)
    _update_featured_bills(today)


def _update_from_social():
    for model in ZEITGEIST_TARGET_MODELS:
        ct = ContentType.objects.get_for_model(model)
        comments = _filter_social_content(Comment, ct)
        votes = _filter_social_content(Vote, ct)

        for created_on, _id in comments + votes:
            ZeitgeistItem.objects.update_or_create(
                target_id=_id,
                target_type=ct,
                defaults={
                    "reason": ZeitgeistItem.REASON_SOCIAL,
                    "created_on": coerce_timezone(created_on),
                },
            )


def _reset_zeitgeist():
    ZeitgeistItem.objects.all().delete()


def _filter_social_content(model: Type[BaseModel], content_type: ContentType) -> list:
    return list(
        model.objects.filter(
            target_type=content_type,
        )
        .order_by(
            "created_on",
        )
        .values_list(
            "created_on",
            "target_id",
        )[:RECENT_ENGAGEMENT_SAMPLE_SIZE]
    )


def _filter_featured_content(model: Type[BaseFeatured], today: datetime.date):
    return (
        model.objects.filter(Q(start__isnull=True) | Q(start__lte=today))
        .filter(Q(end__isnull=True) | Q(end__gte=today))
        .select_related("target")
    )


def _update_featured_people(today: datetime.date):
    for x in _filter_featured_content(FeaturedPerson, today):
        _create_featured_zeitgeist_item(Person, x.start or today, x.target.pk)


def _update_featured_commons_divisions(today: datetime.date):
    for x in _filter_featured_content(FeaturedCommonsDivision, today):
        _create_featured_zeitgeist_item(
            CommonsDivision,
            x.start or today,
            x.target.pk,
        )


def _update_featured_lords_divisions(today: datetime.date):
    for x in _filter_featured_content(FeaturedLordsDivision, today):
        _create_featured_zeitgeist_item(LordsDivision, x.start or today, x.target.pk)


def _update_featured_bills(today: datetime.date):
    for x in _filter_featured_content(FeaturedBill, today):
        _create_featured_zeitgeist_item(Bill, x.start or today, x.target.pk)


def _create_featured_zeitgeist_item(model, created: datetime.date, _id):
    ct = ContentType.objects.get_for_model(model)
    ZeitgeistItem.objects.update_or_create(
        target_id=_id,
        target_type=ct,
        defaults={
            "reason": ZeitgeistItem.REASON_FEATURE,
            "created_on": coerce_timezone(created),
        },
    )
