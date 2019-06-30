from django.contrib import admin

from repository.models import (
    Constituency,
    Mp,
    Party,
)
from repository.models.contact_details import (
    PersonalLinks,
    WebLink,
)


@admin.register(*[Constituency, Party, Mp, PersonalLinks, WebLink])
class DefaultAdmin(admin.ModelAdmin):
    pass
