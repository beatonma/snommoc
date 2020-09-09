"""

"""

import logging
from typing import Type

from celery import shared_task
from django.contrib.contenttypes.models import ContentType

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
from social.models.engagement import (
    RecentBillEngagement,
    RecentCommonsDivisionEngagement,
    RecentLordsDivisionEngagement,
    RecentPersonEngagement,
)

log = logging.getLogger(__name__)


RECENT_ENGAGEMENT_SAMPLE_SIZE = 20


@shared_task
def update_recent_engagement():
    _reset_engagement([
        RecentPersonEngagement,
        RecentCommonsDivisionEngagement,
        RecentLordsDivisionEngagement,
        RecentBillEngagement,
    ])

    blueprints = [
        (Person, RecentPersonEngagement, 'person_id'),
        (CommonsDivision, RecentCommonsDivisionEngagement, 'division_id'),
        (LordsDivision, RecentLordsDivisionEngagement, 'division_id'),
        (Bill, RecentBillEngagement, 'bill_id'),
    ]

    for m, rm, kw in blueprints:
        _update_recent_engagements_for_model(m, rm, kw)


def _filter_targets(model: Type[BaseModel], content_type: ContentType) -> list:
    return model.objects.filter(
        target_type=content_type,
    ).order_by(
        'created_on',
    ).values_list(
        'created_on',
        'target_id'
    )[:RECENT_ENGAGEMENT_SAMPLE_SIZE]


def _update_recent_engagements_for_model(model, recent_model, pk):
    ct = ContentType.objects.get_for_model(model)

    comment_targets = list(_filter_targets(Comment, ct))
    vote_targets = list(_filter_targets(Vote, ct))

    for created, _id in comment_targets + vote_targets:
        kw = {
            pk: _id,
            'created_on': created,
        }
        recent_model.objects.create(**kw)


def _reset_engagement(models):
    """Delete any existing cache of recent engagement."""
    for m in models:
        m.objects.all().delete()
