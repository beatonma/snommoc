from django.contrib import admin

from common.admin import BaseAdmin, get_module_models, register_models_to_default_admin
from repository.apps import RepositoryConfig
from repository.models import Constituency, Person


class RepositoryAdmin(BaseAdmin):
    """
    The DefaultAdmin checks for common fields on the model and applies default behaviour for search, ordering
    and list display.
    """

    default_display_fields = [
        "parliamentdotuk",
        "date",
        "url",
    ]

    default_ordering = [
        "name",
        "-start",
    ]

    default_search_fields = [
        "name",
        "title",
        "parliamentdotuk",
        "person__name",
        "url",
    ]


@admin.register(Constituency)
class ConstituencyAdmin(RepositoryAdmin):
    list_display = [
        "mp",
        "start",
        "end",
    ]

    search_fields = [
        "mp__name",
        "gss_code",
    ]


@admin.register(Person)
class PersonAdmin(RepositoryAdmin):
    ordering = [
        "-active",
        "name",
        "party",
    ]

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = [
            "__str__",
            "house",
            "active",
            "party",
        ]


register_models_to_default_admin(RepositoryConfig.name, RepositoryAdmin)
