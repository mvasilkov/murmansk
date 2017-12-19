from mur.decorators import str_method_from_attr


def test_str_method():
    class File:
        def __init__(self, path, size):
            self.path = path
            self.size = size

    @str_method_from_attr('path')
    class File1(File):
        pass

    @str_method_from_attr('size')
    class File2(File):
        pass

    options = ('/bin/ls', 110080)
    assert str(File1(*options)) == 'File1(path=/bin/ls)'
    assert str(File2(*options)) == 'File2(size=110080)'
