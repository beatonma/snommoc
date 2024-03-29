from django.contrib.auth.models import User

from api.models import ApiKey
from basetest.testcase import LocalTestCase
from social.models import Comment, Vote, VoteType
from social.models.token import SignInServiceProvider, UserToken


class SocialTestCase(
    LocalTestCase,
):
    social_models = [
        ApiKey,
        Comment,
        Comment,
        SignInServiceProvider,
        User,
        UserToken,
        Vote,
        VoteType,
    ]

    def tearDown(self) -> None:
        self.delete_instances_of(*SocialTestCase.social_models)
