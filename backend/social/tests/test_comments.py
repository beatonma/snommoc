import json
import uuid

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework import status

from repository.models import Person
from social.models import Comment
from social.models.token import UserToken
from social.tests.testcase import SocialTestCase
from social.tests.util import create_sample_usertoken
from social.views import contract

_COMMENT = "This is a simple comment"
_TEST_USERNAME = "testuser-comments"


class CommentTests(SocialTestCase):
    """Social comments tests."""

    VIEW_NAME = "social-member-comments"

    def setUp(self, *args, **kwargs) -> None:
        self.valid_token = uuid.uuid4()

        Person.objects.create(parliamentdotuk=4837, name="Aaron Bell", active=True)

        create_sample_usertoken(_TEST_USERNAME, token=self.valid_token)

    def test_post_comment_with_valid_user(self):
        response = self.client.post(
            reverse(CommentTests.VIEW_NAME, kwargs={"pk": 4837}),
            {
                contract.USER_TOKEN: self.valid_token,
                contract.COMMENT_TEXT: _COMMENT,
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
        response = self.client.post(
            reverse(CommentTests.VIEW_NAME, kwargs={"pk": 4837}),
            {
                contract.USER_TOKEN: uuid.uuid4(),
                contract.COMMENT_TEXT: _COMMENT,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNoneCreated(Comment)

    def test_post_comment_with_no_user(self):
        response = self.client.post(
            reverse(CommentTests.VIEW_NAME, kwargs={"pk": 4837}),
            {
                contract.COMMENT_TEXT: _COMMENT,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNoneCreated(Comment)

    def test_post_comment_with_invalid_target(self):
        response = self.client.post(
            reverse(CommentTests.VIEW_NAME, kwargs={"pk": 101012}),
            {
                contract.USER_TOKEN: self.valid_token,
                contract.COMMENT_TEXT: _COMMENT,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNoneCreated(Comment)

    def test_post_comment_with_invalid_comment(self):
        response = self.client.post(
            reverse(CommentTests.VIEW_NAME, kwargs={"pk": 4837}),
            {
                contract.USER_TOKEN: self.valid_token,
                contract.COMMENT_TEXT: "a" * 300,  # Too long
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNoneCreated(Comment)

    def test_get_comments(self):
        user = UserToken.objects.get(username=_TEST_USERNAME)
        Comment.objects.create(
            user=user,
            text=_COMMENT,
            target_type=ContentType.objects.get_for_model(Person),
            target_id=4837,
        )

        # @api_key_required
        response = self.client.get(
            reverse(CommentTests.VIEW_NAME, kwargs={"pk": 4837}),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Disable @api_key_required
        settings.DEBUG = True
        response = self.client.get(
            reverse(CommentTests.VIEW_NAME, kwargs={"pk": 4837}),
        )
        settings.DEBUG = False

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertLengthEquals(data, 1)

        comment = data[0]
        self.assertEqual(comment.get(contract.COMMENT_TEXT), _COMMENT)
        self.assertEqual(comment.get(contract.USER_NAME), _TEST_USERNAME)

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
        response = self.client.post(
            reverse(CommentTests.VIEW_NAME, kwargs={"pk": 4837}),
            {
                contract.USER_TOKEN: self.valid_token,
                contract.COMMENT_TEXT: (
                    'blah <a href="https://snommoc.org/">just the text</a><script>'
                ),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment: Comment = Comment.objects.first()
        self.assertEqual(comment.text, "blah just the text")

    def test_post_comment_with_html_is_flagged(self):
        response = self.client.post(
            reverse(CommentTests.VIEW_NAME, kwargs={"pk": 4837}),
            {
                contract.USER_TOKEN: self.valid_token,
                contract.COMMENT_TEXT: (
                    '<a href="https://snommoc.org/">This should be flagged for'
                    " review</a><script>"
                ),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment: Comment = Comment.objects.first()
        self.assertEqual(comment.flagged, True)

    def test_post_comment_with_no_html_is_not_flagged(self):
        response = self.client.post(
            reverse(CommentTests.VIEW_NAME, kwargs={"pk": 4837}),
            {
                contract.USER_TOKEN: self.valid_token,
                contract.COMMENT_TEXT: _COMMENT,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment: Comment = Comment.objects.first()
        self.assertEqual(comment.flagged, False)

    def tearDown(self) -> None:
        self.delete_instances_of(
            # ApiKey,
            # Comment,
            # Comment,
            Person,
            *SocialTestCase.social_models,
            # UserToken,
            # check_instances=False,
        )
        # super().tearDown()
