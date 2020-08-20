"""
Source: https://gist.github.com/pzrq/460424c9382dd50d02b8
"""


def get_all_subclasses(python_class):
    """
    Helper function to get all the subclasses of a class.
    :param python_class: Any Python class that implements __subclasses__()
    """
    python_class.__subclasses__()

    subclasses = set()
    check_these = [python_class]

    while check_these:
        parent = check_these.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                check_these.append(child)

    return sorted(subclasses, key=lambda x: x.__name__)


def get_concrete_models(base_model):
    """
    Helper function to get all concrete models
    that are subclasses of base_model
    in sorted order by name.
    :param base_model: A Django models.Model instance.
    """
    found = get_all_subclasses(base_model)

    def filter_func(model):
        meta = getattr(model, '_meta', '')
        if getattr(meta, 'abstract', True):
            # Skip meta classes
            return False
        if '_Deferred_' in model.__name__:
            # See deferred_class_factory() in django.db.models.query_utils
            # Catches when you do .only('attr') on a queryset
            return False
        return True

    subclasses = list(filter(filter_func, found))
    return sorted(subclasses, key=lambda x: x.__name__)
