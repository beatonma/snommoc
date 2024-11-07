import logging

from api import status
from django.http import HttpRequest
from ninja import Router

from . import schema

log = logging.getLogger(__name__)
router = Router(tags=["Account"])


@router.get("/", response=schema.UserAccount)
def get_account(request: HttpRequest, token: str):
    return schema.resolve_user_token(token)


@router.post("/", response=schema.UserAccount)
def rename_account(request: HttpRequest, data: schema.RenameAccount):
    user = data.resolve_user_token(username=data.username)
    if data.username != data.new_username:
        user.username = data.new_username
        user.full_clean()
        user.save()
        log.info(f"Account renamed: {data.username} -> {data.new_username}")
    return status.HTTP_200_OK, user


@router.delete("/", response={202: None})
def delete_account(request: HttpRequest, data: schema.DeleteAccount):
    user = data.resolve_user_token()
    user.mark_pending_deletion()
    user.save()
    log.info(f"Account marked for deletion: {user}")
    return status.HTTP_202_ACCEPTED, None
