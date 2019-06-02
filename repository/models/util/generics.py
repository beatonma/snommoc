class GetSubclassesMixin(object):
    @classmethod
    def get_subclasses(cls):
        return {'name__in': [c.__name__ for c in cls.__subclasses__()]}
