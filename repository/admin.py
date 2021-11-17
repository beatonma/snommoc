from django.contrib import admin

from common.admin import BaseAdmin, register_models_to_default_admin
from repository.apps import RepositoryConfig
from repository.models import (
    Constituency,
    ConstituencyAlsoKnownAs,
    Party,
    PartyAlsoKnownAs,
    Person,
    PersonAlsoKnownAs,
)
from repository.models.party import PartyTheme


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

    default_readonly_fields = BaseAdmin.default_readonly_fields + [
        "name",
        "title",
        "parliamentdotuk",
        "label",
        "date",
        "start",
        "end",
    ]


class ReadOnlyRepositoryAdmin(RepositoryAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        fields = model._meta.fields
        self.readonly_fields = [x.name for x in fields]


@admin.register(
    ConstituencyAlsoKnownAs,
    Party,
    PartyAlsoKnownAs,
    PersonAlsoKnownAs,
    PartyTheme,
)
class DefaultEditableAdmin(RepositoryAdmin):
    pass


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

    readonly_fields = [
        "gss_code",
        "ordinance_survey_name",
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


register_models_to_default_admin(RepositoryConfig.name, ReadOnlyRepositoryAdmin)
