from celery import shared_task
from crawlers import caches
from crawlers.context import TaskContext
from crawlers.network import JsonCache, json_cache
from crawlers.parliamentdotuk.tasks.lda import endpoints
from crawlers.parliamentdotuk.tasks.lda.lda_client import foreach
from notifications.models.task_notification import TaskNotification, task_notification
from repository.models import Constituency

from . import schema


@shared_task
@task_notification(label="Update constituencies")
@json_cache(caches.CONSTITUENCIES)
def update_constituencies(
    follow_pagination=True,
    cache: JsonCache | None = None,
    notification: TaskNotification | None = None,
    force_update: bool = False,
    **kwargs,
) -> None:
    context = TaskContext(notification=notification, cache=cache)

    def build_constituency(data: schema.Constituency, _context: TaskContext):
        Constituency.objects.update_or_create(
            parliamentdotuk=data.parliamentdotuk,
            defaults={
                "name": data.name,
                "gss_code": data.gss_code,
                "ordinance_survey_name": data.os_name,
                "constituency_type": data.type,
                "start": data.started_date,
                "end": data.ended_date,
            },
        )

    foreach(
        endpoints.CONSTITUENCIES_BASE_URL,
        item_schema_type=schema.Constituency,
        item_func=build_constituency,
        context=context,
        follow_pagination=follow_pagination,
    )
