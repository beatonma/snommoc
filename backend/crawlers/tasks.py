"""
Tasks that combine sub-tasks from multiple sources.
"""

from crawlers import caches
from crawlers.context import TaskContext, task_context
from crawlers.parliamentdotuk.tasks.openapi.members.member_portrait import (
    update_official_member_portraits,
)
from crawlers.wikipedia.tasks.member_portrait import update_wikipedia_member_portraits
from repository.models import Person


@task_context(cache_name=caches.MEMBER_PORTRAITS)
def update_member_portraits(context: TaskContext):
    members = Person.objects.active()

    update_official_member_portraits(members, context=context)
    update_wikipedia_member_portraits(
        members.filter(memberportrait__isnull=True, wikipedia__isnull=False),
        context=context,
    )
