import logging
import math
import random
import uuid
from datetime import datetime, timedelta
from typing import List

from django.contrib.auth.models import User
from django.db.models import Model
from util.time import tzdatetime


def create_sample_user(
    username: str = "default-test-user",
    password: str = uuid.uuid4().hex,
    email: str = "testuser@snommoc.org",
) -> User:
    print(f"create_sample_user: [{username}|{password}|{email}]")
    user = User.objects.create(username=username, password=password, email=email)
    user.set_password(password)
    user.save()
    return user


def log_dump(obj, logger: logging.Logger):
    """Expects obj to be an instance of Model, or a collection of Model instances"""
    if isinstance(obj, Model):
        logger.debug(f"MODEL: [{obj.__class__.__name__}] {obj}")
        fields = obj._meta.get_fields(include_parents=True, include_hidden=True)
        logger.debug(f"FIELDS: {[field.name for field in fields]}")
        for field in fields:
            try:
                logger.debug(f" FIELD: [{field.name}] {getattr(obj, field.name)}")
            except Exception as e:
                logger.warning(f'  Unable to read value for field="{field.name}"')
                logger.error(e)
    else:
        logger.debug("Unpacking model collection...")
        for model_instance in obj:
            log_dump(model_instance, logger)


def create_sample_dates(
    count: int = 10,
    start: datetime = tzdatetime(2011, 5, 16),
    end: datetime = tzdatetime(2020, 5, 16),
) -> List[datetime]:
    period = end - start
    max_step_size = max(1, math.ceil(period.days / count))

    dates = []
    previous = start
    for n in range(0, count):
        random.randrange(1, max_step_size)
        previous = previous + timedelta(days=random.randrange(1, max_step_size))

        dates.append(previous)

    return dates


def dump_urlpatterns(urlpatterns, level: int = 0):
    if level == 0:
        print("urlpatterns: [")
    else:
        print(f'{" "*level}[')

    for u in urlpatterns:
        if hasattr(u, "url_patterns"):
            dump_urlpatterns(u.url_patterns, level + 2)
        else:
            print(f'{" "*(level + 2)}{u.name}: {u.pattern}')

    print(f'{" "*level}]')
