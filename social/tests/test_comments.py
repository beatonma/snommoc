"""

"""
import json
import logging
import uuid

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status

from api.models import ApiKey
from api.tests.views import with_api_key
from basetest.testcase import LocalTestCase
from repository.models import Person
from social.models import Comment
from social.models.token import UserToken

log = logging.getLogger(__name__)


_COMMENT = 'This is a simple comment'


class CommentTests(LocalTestCase):

    @with_api_key
    def setUp(self, *args, **kwargs) -> None:
        self.valid_token = uuid.uuid4()
        self.params = kwargs.get('params')

        Person.objects.create(
            parliamentdotuk=4837,
            name='Aaron Bell',
            active=True
        ).save()
        UserToken.objects.create(
            token=self.valid_token,
            username='testuser',
        ).save()

    def test_post_comment_with_valid_user(self):
        response = self.client.post(
            reverse('social-member-comments', kwargs={'pk': 4837}),
            {
                'token': self.valid_token,
                'text': _COMMENT,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comments = Comment.objects.all()
        self.assertLengthEquals(comments, 1)

        comment = comments.first()
        self.assertEqual(comment.user.username, 'testuser')
        self.assertEqual(comment.text, _COMMENT)

    def test_post_comment_with_invalid_user(self):
        response = self.client.post(
            reverse('social-member-comments', kwargs={'pk': 4837}),
            {
                'token': uuid.uuid4(),
                'text': _COMMENT,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertLengthEquals(Comment.objects.all(), 0)

    def test_post_comment_with_no_user(self):
        response = self.client.post(
            reverse('social-member-comments', kwargs={'pk': 4837}),
            {
                'text': _COMMENT,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertLengthEquals(Comment.objects.all(), 0)

    def test_post_comment_with_invalid_target(self):
        response = self.client.post(
            reverse('social-member-comments', kwargs={'pk': 101012}),
            {
                'token': self.valid_token,
                'text': _COMMENT,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertLengthEquals(Comment.objects.all(), 0)

    def test_post_comment_with_invalid_comment(self):
        response = self.client.post(
            reverse('social-member-comments', kwargs={'pk': 4837}),
            {
                'token': self.valid_token,
                'text': 'a'*300,  # Too long
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertLengthEquals(Comment.objects.all(), 0)

    def test_get_comments(self):
        user = UserToken.objects.get(username='testuser')
        Comment.objects.create(
            user=user,
            text=_COMMENT,
            target_type=ContentType.objects.get_for_model(Person),
            target_id=4837,
        ).save()

        settings.DEBUG = True  # Disable @api_key_required
        response = self.client.get(
            reverse('social-member-comments', kwargs={'pk': 4837}),
        )
        settings.DEBUG = False

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertLengthEquals(data, 1)

        comment = data[0]
        self.assertEqual(comment.get('comment'), _COMMENT)
        self.assertEqual(comment.get('username'), 'testuser')

    def tearDown(self) -> None:
        self.delete_instances_of(
            ApiKey,
            UserToken,
            Comment,
            Person,
        )
