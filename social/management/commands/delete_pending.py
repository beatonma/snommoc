from social.tasks import delete_expired_models
from util.management.async_command import AsyncCommand


class Command(AsyncCommand):
    def handle(self, *args, **options):
        func = delete_expired_models

        self.handle_async(func, *args, **options)
