from django.contrib import admin

from api.models import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ['user', 'enabled', 'created']
    readonly_fields = ['key']
