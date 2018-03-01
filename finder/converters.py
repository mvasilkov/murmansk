class ModelNameConverter:
    regex = '[A-Z][A-Za-z]*'

    @staticmethod
    def to_python(value: str):
        return value

    @staticmethod
    def to_url(value: str):
        return value


class BooleanConverter:
    regex = 'True|False'

    @staticmethod
    def to_python(value: str):
        return value == 'True'

    @staticmethod
    def to_url(value: bool):
        return str(value)
