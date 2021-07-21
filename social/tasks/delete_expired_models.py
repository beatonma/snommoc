import logging

from celery import shared_task

from notifications.models.task_notification import task_notification
from social.models.mixins import DeletionPendingMixin
from util.models.generics import get_all_subclasses

log = logging.getLogger(__name__)


@shared_task
@task_notification(label="Delete expired models")
def delete_expired_models(**kwargs):
    model_classes = get_all_subclasses(DeletionPendingMixin)
    for MC in model_classes:
        log.info(f"Checking class {MC} for expired instances...")
        pending_deletion = MC.objects.filter(pending_deletion=True)

        if pending_deletion.count() == 0:
            log.info("  No instances pending deletion.")

        for x in pending_deletion:
            log.info(f'  "{x}" expires in {x.hours_until_expired()} hours!')
        expired = [x for x in pending_deletion if x.is_expired()]

        for x in expired:
            log.warning(f"  Deleting {x}")
            x.delete()
