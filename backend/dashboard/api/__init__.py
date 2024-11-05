import logging

from dashboard.api.schema import DashboardTaskNotificationSchema
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.pagination import paginate
from notifications.models import TaskNotification

from .constituencies import router as constituencies_router
from .tasks import router as tasks_router
from .zeitgeist import router as zeitgeist_router

api = NinjaAPI(
    title="Dashboard API",
    docs_url="/docs/",
    docs_decorator=staff_member_required,
)
api.add_router("tasks/", tasks_router)
api.add_router("constituencies/", constituencies_router)
api.add_router("zeitgeist/", zeitgeist_router)


@api.get(
    "recent-notifications/",
    response=list[DashboardTaskNotificationSchema],
)
@paginate
def recent_notifications(request: HttpRequest):
    return TaskNotification.objects.filter(level__gte=logging.INFO).order_by(
        "-created_on"
    )
