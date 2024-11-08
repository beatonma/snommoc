from api.models import ApiKey
from basetest.testcase import LocalTestCase
from django.contrib.auth.models import User
from social.models import Comment, Vote
from social.models.token import UserToken


class SocialTestCase(
    LocalTestCase,
):
    social_models = [
        ApiKey,
        Comment,
        Comment,
        User,
        UserToken,
        Vote,
    ]

    def tearDown(self) -> None:
        self.delete_instances_of(*SocialTestCase.social_models)
