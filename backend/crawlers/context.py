from crawlers.network import JsonCache
from notifications.models import TaskNotification
from requests import Session


class TaskContext:
    def __init__(
        self,
        cache: JsonCache | None,
        notification: TaskNotification | None,
        session: Session | None = None,
    ):
        self.notification = notification
        self.cache = cache
        self.session = session
