from social.tasks import delete_expired_models
from util.management.task_command import TaskCommand


class Command(TaskCommand):
    def handle(self, *args, **options):
        func = delete_expired_models

        self.handle_async(func, *args, **options)
