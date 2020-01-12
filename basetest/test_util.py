import logging
import uuid

from django.contrib.auth.models import User
from django.db.models import Model


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
        password=uuid.uuid4().hex,
        email='testuser@snommoc.org'
) -> User:
    user = User.objects.create(
        username=username,
        password=password,
        email=email)
    user.set_password(password)
    user.save()
    return user


def log_dump(obj, logger: logging.Logger):
    """Expects obj to be an instance of Model, or a collection of Model instances"""
    if isinstance(obj, Model):
        logger.debug(f'MODEL: [{obj.__class__.__name__}] {obj}')
        fields = obj._meta.get_fields(include_parents=True, include_hidden=True)
        logger.debug(f'FIELDS: {[field.name for field in fields]}')
        for field in fields:
            try:
                logger.debug(f' FIELD: [{field.name}] {getattr(obj, field.name)}')
            except Exception as e:
                logger.warning(f'  Unable to read value for field="{field.name}"')
                logger.error(e)
    else:
        logger.debug('Unpacking model collection...')
        for model_instance in obj:
            log_dump(model_instance, logger)
