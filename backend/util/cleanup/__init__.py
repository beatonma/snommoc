"""
Function @decorators and class mixins which may be useful for refactoring.

@unused: Raises an exception if the decorated function is called.
UnusedClass: Raises an exception if the class is instantiated.

@deprecated: Logs a deprecation warning when the decorated function is called.
Deprecated: Logs a deprecation warning when the class is instantiated.
"""

import logging

log = logging.getLogger(__name__)


class UnusedException(BaseException):
    pass


class UnusedClass:
    """Utility mixin to mark a class as unused.

    If a class is currently unused but may be used again in the future, it should
    inherit Unused. This allows us to search for unused classes later and decide
    if we still want to keep them.

    Any implementation of this class will  raise UnusedException when instantiated -
    you must remove the inheritance if you want to use the class.
    """

    def __init__(self, *args, **kwargs):
        raise UnusedException(
            f"Class {self.__class__.__name__} is marked as unused! Remove UnusedClass mixin to enable it again."
        )


def unused(func):
    """Marks function as unused and raises UnusedException if it is called."""

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
