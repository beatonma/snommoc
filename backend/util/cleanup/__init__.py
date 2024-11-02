"""
When inspecting code we may find classes or functions that are not currently in use but we do not want to delete them
as they may be useful later. Such classes should be updated to inherit UnusedClass, and such functions should be marked
with the @unused decorator. This allows
"""

import logging

log = logging.getLogger(__name__)


class UnusedException(BaseException):
    pass


class UnusedClass:
    """Utility base class to mark a child class as unused.

    If a class is currently unused but may be used again in the future, it should inherit Unused. This allows us to
    search for unused classes later and decide if we still want to keep them.

    A child of this class will raise UnusedException when instantiated - you must remove the inheritance if you want
    to use the class.
    """

    def __init__(self, *args, **kwargs):
        raise UnusedException(
            f"Class {self.__class__.__name__} is marked as unused! Remove inheritance of Unused to enable it again."
        )


def unused(func):
    def f(*args, **kwargs):
        raise UnusedException(
            f"Function {func.__name__} is marked as unused! Remove @unused decorator to enable it again."
        )

    return f


class Deprecated:
    def __init__(self, *args, **kwargs):
        log.warning(f"DEPRECATED: Class {self.__class__.__name__}")


def deprecated(func):
    def f(*args, **kwargs):
        log.warning(f"DEPRECATED: Function {func.__name__}")
        return func(*args, **kwargs)

    return f
