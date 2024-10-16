from django.contrib.auth.models import User

READ_SNOMMOC_API = 'read_snommoc_api'


def has_read_snommoc_api_permission(user: User) -> bool:
    return user.has_perm(f'api.{READ_SNOMMOC_API}')
