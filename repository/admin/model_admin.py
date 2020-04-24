from typing import List

from django.apps import apps
from django.contrib import admin
from django.db import models

from repository.models import (
    Constituency,
    CommonsDivision,
    LordsDivision,
    Party,
)
from repository.models.person import Person

# Models that have an explicit ModelAdmin associated with them
# Any models not in this list will have a generic ModelAdmin.
DEDICATED_ADMIN_MODELS = [
    Constituency,
    Person,
    Party,
    CommonsDivision,
    LordsDivision,
]
repository_config = apps.get_app_config('repository')
GENERIC_ADMIN_MODELS: List[models.Model] = [
    model for model in repository_config.get_models()
    if model not in DEDICATED_ADMIN_MODELS
]


class DefaultAdmin(admin.ModelAdmin):
    save_on_top = True
    pass


for model in GENERIC_ADMIN_MODELS:
    try:
        admin.site.register(model, DefaultAdmin)
    except admin.sites.AlreadyRegistered:
        pass


@admin.register(Constituency)
class ConstituencyAdmin(DefaultAdmin):
    ordering = ['name']
    list_display = [
        'name',
        'mp',
        'gss_code',
        'start',
        'end',
    ]
    search_fields = [
        'name',
        'gss_code',
    ]


@admin.register(Person)
class PersonAdmin(DefaultAdmin):
    list_display = [
        'name',
        'house',
        'active',
        'party',
    ]

    search_fields = [
        'name',
    ]


@admin.register(CommonsDivision, LordsDivision)
class DivisionAdmin(DefaultAdmin):
    search_fields = [
        'parliamentdotuk',
    ]


@admin.register(Party)
class PartyAdmin(DefaultAdmin):
    list_display = [
        'name',
        'parliamentdotuk',
    ]

    search_fields = [
        'name',
    ]
