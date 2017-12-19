def str_method_from_attr(name):
    def decorator(cls):
        def str_method(self):
            return '%s(%s=%s)' % (self.__class__.__name__, name, getattr(self, name))

        cls.__str__ = str_method
        return cls

    return decorator
