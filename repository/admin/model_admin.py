from django.contrib import admin
from django.contrib.admin import TabularInline

from repository.models.contact_details import (
    Links,
    WebLink,
)

from repository.models import (
    # Mp,
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
])
class DefaultAdmin(admin.ModelAdmin):
    pass


# @admin.register(Mp)
# class MpAdmin(DefaultAdmin):
#     ordering = ['person__family_name']


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
    ordering = [
        'family_name',
    ]
    inlines = [
        InterestInline,
    ]
