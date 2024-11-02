from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType

READ_SNOMMOC_API = "read_snommoc_api"


def has_read_snommoc_api_permission(user: AbstractUser) -> bool:
    return user.has_perm(f"api.{READ_SNOMMOC_API}")


def grant_read_snommoc_api(user: AbstractUser):
    from .models import ApiKey

    content_type = ContentType.objects.get_for_model(ApiKey)
    read_permission = Permission.objects.get(
        codename=READ_SNOMMOC_API,
        content_type=content_type,
    )
    user.user_permissions.add(read_permission)
    user.save()
