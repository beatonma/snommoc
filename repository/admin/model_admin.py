from django.contrib import admin
from django.contrib.admin import TabularInline

from repository.models.contact_details import (
    Links,
    WebLink,
)

from repository.models import (
    Mp,
    Party,
    Constituency,
)


from repository.models.interests import Interest
from repository.models.person import Person


class InterestInline(TabularInline):
    model = Interest


@admin.register(*[
    Party,
    Links,
    WebLink,
    Mp,
])
class DefaultAdmin(admin.ModelAdmin):
    pass


@admin.register(Constituency)
class ConstituencyAdmin(DefaultAdmin):
    ordering = ['name']
    list_display = [
        'name',
        'mp',
        'start',
        'end',
    ]

@admin.register(Person)
class PersonAdmin(DefaultAdmin):
    inlines = [
        InterestInline,
    ]
