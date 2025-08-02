import uuid

from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, transaction

from api import status
from basetest.testcase import DatabaseTestCase
from repository.models import Person
from repository.tests.data.create import create_sample_person
from social.models import Comment
from social.models.token import UserToken
from social.tests.util import create_sample_usertoken, reverse_api

_COMMENT = "This is a simple comment"
_TEST_USERNAME = "comments"


VIEWNAME_CREATE_COMMENT = reverse_api("create_comment")
VIEWNAME_DELETE_COMMENT = reverse_api("delete_comment")


class CommentTests(DatabaseTestCase):
    """Social comments tests."""

    def post_json(self, data: dict):
        return self.client.post(
            VIEWNAME_CREATE_COMMENT,
            data,
            content_type="application/json",
        )

    def setUp(self, *args, **kwargs) -> None:
        self.valid_token = uuid.uuid4()

        create_sample_person(parliamentdotuk=4837, name="Aaron Bell")

        create_sample_usertoken(_TEST_USERNAME, token=self.valid_token)

    def test_post_comment_with_valid_user(self):
        response = self.post_json(
            {
                "token": self.valid_token,
                "text": _COMMENT,
                "target": "person",
                "target_id": 4837,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comments = Comment.objects.all()
        self.assertLengthEquals(comments, 1)

        comment: Comment = comments.first()
        self.assertEqual(comment.user.username, _TEST_USERNAME)
        self.assertEqual(comment.text, _COMMENT)

        # Ensure comment points to the correct target
        self.assertEqual(comment.target_id, 4837)
        self.assertEqual(comment.target_type, ContentType.objects.get_for_model(Person))

        self.assertEqual(comment.target, Person.objects.get(pk=4837))

    def test_post_comment_with_invalid_user(self):
        response = self.post_json(
            {
                "token": uuid.uuid4(),
                "text": _COMMENT,
                "target": "person",
                "target_id": 4837,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNoneCreated(Comment)

    def test_post_comment_with_no_user(self):
        response = self.post_json(
            {
                "text": _COMMENT,
                "target": "person",
                "target_id": 4837,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertNoneCreated(Comment)

    def test_post_comment_with_invalid_target(self):
        response = self.post_json(
            {
                "token": self.valid_token,
                "text": _COMMENT,
                "target": "person",
                "target_id": 101012,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNoneCreated(Comment)

    def test_post_comment_with_invalid_comment(self):
        response = self.post_json(
            {
                "token": self.valid_token,
                "text": "a" * 300,  # Too long
                "target": "person",
                "target_id": 4837,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertNoneCreated(Comment)

    def test_comment_unique_per_user_per_object(self):
        user = UserToken.objects.get(username=_TEST_USERNAME)
        Comment.objects.create(
            user=user,
            text=_COMMENT,
            target_type=ContentType.objects.get_for_model(Person),
            target_id=4837,
        )

        Comment.objects.create(
            user=user,
            text="different comment",
            target_type=ContentType.objects.get_for_model(Person),
            target_id=4837,
        )

        # Different user, same target and comment
        Comment.objects.create(
            user=create_sample_usertoken(),
            text=_COMMENT,
            target_type=ContentType.objects.get_for_model(Person),
            target_id=4837,
        )

        # Duplicate of first comment
        with transaction.atomic():
            self.assertRaises(
                IntegrityError,
                lambda: Comment.objects.create(
                    user=user,
                    text=_COMMENT,
                    target_type=ContentType.objects.get_for_model(Person),
                    target_id=4837,
                ),
            )

    def test_post_comment_with_html_is_stripped(self):
        response = self.post_json(
            {
                "token": self.valid_token,
                "text": (
                    'blah <a href="https://snommoc.org/">just the text</a><script>'
                ),
                "target": "person",
                "target_id": 4837,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment: Comment = Comment.objects.first()
        self.assertEqual(comment.text, "blah just the text")

    def test_post_comment_with_html_is_flagged(self):
        response = self.post_json(
            {
                "token": self.valid_token,
                "text": (
                    '<a href="https://snommoc.org/">This should be flagged for'
                    " review</a><script>"
                ),
                "target": "person",
                "target_id": 4837,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment: Comment = Comment.objects.first()
        self.assertTrue(comment.flagged)

    def test_post_comment_with_no_html_is_not_flagged(self):
        response = self.post_json(
            {
                "token": self.valid_token,
                "text": _COMMENT,
                "target": "person",
                "target_id": 4837,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment: Comment = Comment.objects.first()
        self.assertFalse(comment.flagged)
