from surface.tasks import update_zeitgeist
from util.management.task_command import TaskCommand


class Command(TaskCommand):
    def handle(self, *args, **options):
        func = update_zeitgeist

        self.handle_async(func, *args, **options)
