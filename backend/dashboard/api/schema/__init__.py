from datetime import datetime

from ninja import Schema


class DashboardTaskNotificationSchema(Schema):
    title: str | None
    content: str | None
    complete: bool
    failed: bool
    created_on: datetime
    finished_at: datetime | None
    level: int
