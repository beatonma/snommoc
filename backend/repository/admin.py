from common.admin import BaseAdmin, register_models_to_default_admin
from django.contrib import admin
from django.db.models import QuerySet
from repository.apps import RepositoryConfig
from repository.models import (
    Constituency,
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

    editable_fields = []

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        fields = model._meta.fields
        self.readonly_fields = [
            x.name for x in fields if x.name not in self.editable_fields
        ]


@admin.register(
    Party,
    PartyAlsoKnownAs,
    PersonAlsoKnownAs,
    PartyTheme,
)
class DefaultEditableAdmin(RepositoryAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        readonly_fields = ["parliamentdotuk", "created_on", "modified_on"]
        fields = model._meta.fields
        self.readonly_fields = [x.name for x in fields if x.name in readonly_fields]


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
        "-is_active",
        "name",
        "party",
    ]
    list_display = [
        "__str__",
        "house",
        "is_active",
        "party",
    ]
    editable_fields = [
        "wikipedia",
    ]

    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset()
        qs: QuerySet = qs.select_related(
            "party",
            "house",
        )

        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


register_models_to_default_admin(RepositoryConfig.name, RepositoryAdmin)
