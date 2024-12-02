import uuid

from basetest.testcase import DatabaseTestCase
from repository.tests.data.create import create_sample_person
from social.tests import reverse_api
from social.tests.util import (
    create_sample_comment,
    create_sample_usertoken,
    create_sample_vote,
)

_VALID_USER = "get-social-valid-user"

VIEWNAME_GET = reverse_api("get_social_content")


class GetSocialAllTests(DatabaseTestCase):
    """Tests for social content endpoint /all/"""

    def setUp(self, *args, **kwargs) -> None:
        self.valid_token = uuid.uuid4()

        self.target_person_one = create_sample_person(
            parliamentdotuk=4837,
            name="Aaron Bell",
        )

        self.target_person_two = create_sample_person(1423, "Boris Johnson")

        self.valid_user = create_sample_usertoken(
            username=_VALID_USER,
            token=self.valid_token,
            enabled=True,
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
            VIEWNAME_GET,
            data={
                "target": "person",
                "target_id": 1423,
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertDictEqual(
            response.json(),
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
            VIEWNAME_GET,
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
            VIEWNAME_GET,
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

    def assertSocialDataEqual(self, response, expected):
        """
        expected_comments should be a list of (comment_text, username) tuples.
        """

        data = response.json()

        # Replace timestamped comments with (text,username) tuples.
        actual_comments = [[x["text"], x["username"]] for x in data.get("comments")]
        data["comments"] = actual_comments

        self.assertDictEqual(
            data,
            expected,
        )
