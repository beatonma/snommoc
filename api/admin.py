from django.contrib import admin

from api.models import ApiKey
from common.admin import BaseAdmin


@admin.register(ApiKey)
class ApiKeyAdmin(BaseAdmin):
    list_display = ["user", "enabled", "created"]
    readonly_fields = ["key"]
