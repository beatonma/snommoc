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
        # check_required_fields(
        #     json_data,
        #     contract.ABOUT,
        #     contract.NAME,
        # )
        #
        # puk = get_parliamentdotuk_id(json_data)
        # name = get_str(json_data, contract.NAME)
        #
        # Constituency.objects.update_or_create(
        #     parliamentdotuk=puk,
        #     defaults={
        #         "name": name,
        #         "gss_code": get_str(json_data, contract.GSS_CODE),
        #         "ordinance_survey_name": get_str(
        #             json_data,
        #             contract.ORDINANCE_SURVEY_NAME,
        #             default="",
        #         ),
        #         "constituency_type": get_str(json_data, contract.TYPE),
        #         "start": get_date(json_data, contract.DATE_STARTED),
        #         "end": get_date(json_data, contract.DATE_ENDED),
        #     },
        # )

    foreach(
        endpoints.CONSTITUENCIES_BASE_URL,
        item_schema_type=schema.Constituency,
        item_func=build_constituency,
        context=context,
        follow_pagination=follow_pagination,
    )
