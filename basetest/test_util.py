import uuid

from django.conf import settings
from django.contrib.auth.models import User

from api import contract


def inject_context_manager(cls):
    """
    Add simple __enter__, __exit__ methods to the given class so that we
    can use the class in a `with` statement for VISUALLY block-scoped tests.

    WARNING: Stuff inside the block can still affect stuff outside,
    it's just indented to make tests easier to read.
    """
    cls.__enter__ = lambda x: x
    cls.__exit__ = lambda x, a, b, c: None


def create_test_user(
        username='testuser',
        password=uuid.uuid4(),
        email='testuser@snommoc.org'
) -> User:
    user = User.objects.create(
        username=username,
        password=password,
        email=email)
    user.save()
    return user
