from django.apps import AppConfig


class RepositoryConfig(AppConfig):
    name = "repository"

    def ready(self):
        from repository.signals import (  # noqa
            update_constituencycandidate_party_when_partyaka_canonical_changed,
        )
