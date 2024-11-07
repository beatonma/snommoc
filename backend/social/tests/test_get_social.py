import json
import uuid

from django.urls import reverse
from repository.models import Person
from social.models.token import UserToken
from social.tests.testcase import SocialTestCase
from social.tests.util import (
    create_sample_comment,
    create_sample_usertoken,
    create_sample_vote,
)

_VALID_USER = "get-social-valid-user"

VIEWNAME_GET = "social_api-2.0:get_social_content"


class GetSocialAllTests(SocialTestCase):
    """Tests for social content endpoint /all/"""

    def setUp(self, *args, **kwargs) -> None:
        self.valid_token = uuid.uuid4()

        self.target_person_one, _ = Person.objects.get_or_create(
            parliamentdotuk=4837,
            name="Aaron Bell",
            active=True,
        )

        self.target_person_two, _ = Person.objects.get_or_create(
            parliamentdotuk=1423,
            name="Boris Johnson",
            active=True,
        )

        self.valid_user, _ = UserToken.objects.get_or_create(
            token=self.valid_token,
            username=_VALID_USER,
        )

    def create_sample_data(self):
        create_sample_comment(self.target_person_one, self.valid_user, "first comment")
        create_sample_comment(self.target_person_one, self.valid_user, "second comment")
        create_sample_comment(
            self.target_person_one,
            create_sample_usertoken(username="another_user"),
            "third comment",
        )
        create_sample_comment(
            self.target_person_two, self.valid_user, "comment on different target!"
        )

        # Votes for actual target
        create_sample_vote(self.target_person_one, self.valid_user, "aye")
        create_sample_vote(self.target_person_one, create_sample_usertoken(), "aye")
        create_sample_vote(self.target_person_one, create_sample_usertoken(), "no")

        # Votes on different target
        create_sample_vote(self.target_person_two, self.valid_user, "aye")
        create_sample_vote(self.target_person_two, create_sample_usertoken(), "no")
        create_sample_vote(self.target_person_two, create_sample_usertoken(), "no")

    def test_get_all_empty(self):
        response = self.client.get(
            reverse(
                VIEWNAME_GET,
            ),
            data={
                "target": "person",
                "target_id": 1423,
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(
            response.content,
            {
                "title": "Boris Johnson",
                "comments": [],
                "votes": {},
                "user_vote": None,
            },
        )

    def test_get_all_with_content_no_user_token(self):
        self.create_sample_data()
        response = self.client.get(
            reverse(
                VIEWNAME_GET,
            ),
            data={
                "target": "person",
                "target_id": 4837,
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertSocialDataEqual(
            response,
            {
                "title": "Aaron Bell",
                "votes": {
                    "aye": 2,
                    "no": 1,
                },
                "comments": [
                    ["first comment", _VALID_USER],
                    ["second comment", _VALID_USER],
                    ["third comment", "another_user"],
                ],
                "user_vote": None,
            },
        )

    def test_get_all_with_content_with_user_token(self):
        """If user has voted on the target then their vote_type should be included in response"""
        self.create_sample_data()

        response = self.client.get(
            reverse(VIEWNAME_GET),
            data={
                "token": self.valid_token,
                "target": "person",
                "target_id": 4837,
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertSocialDataEqual(
            response,
            {
                "title": "Aaron Bell",
                "votes": {
                    "aye": 2,
                    "no": 1,
                },
                "comments": [
                    ["first comment", _VALID_USER],
                    ["second comment", _VALID_USER],
                    ["third comment", "another_user"],
                ],
                "user_vote": "aye",
            },
        )

    def tearDown(self) -> None:
        self.delete_instances_of(
            Person,
            *SocialTestCase.social_models,
        )

    def assertSocialDataEqual(self, response, expected):
        """
        expected_comments should be a list of (comment_text, username) tuples.
        """

        data = json.loads(response.content)

        # Replace timestamped comments with (text,username) tuples.
        actual_comments = [[x["text"], x["username"]] for x in data.get("comments")]
        data["comments"] = actual_comments

        print(json.dumps(data, indent=1))
        print(json.dumps(expected, indent=1))

        self.assertDictEqual(
            data,
            expected,
        )
