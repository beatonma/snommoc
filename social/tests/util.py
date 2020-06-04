"""

"""

import logging
import uuid

from social.models.token import UserToken

log = logging.getLogger(__name__)


def create_usertoken(username=None, token=uuid.uuid4):
    if username is None:
        username = uuid.uuid4().hex[:6]

    if callable(token):
        token = token()

    usertoken = UserToken.objects.create(
        username=username,
        token=token,
        provider_account_id=uuid.uuid4(),
    )
    usertoken.save()
    return usertoken
