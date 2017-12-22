import re

from directory.models import _picture_path
import pytest


def test_picture_path():
    filename = '[a-f0-9]/[a-f0-9]{24}'
    assert re.fullmatch(r'%s\.gif' % filename, _picture_path(None, 'a.gif')) is not None
    assert re.fullmatch(r'%s\.jpeg' % filename, _picture_path(None, 'a.jpg')) is not None
    assert re.fullmatch(r'%s\.jpeg' % filename, _picture_path(None, 'a.jpeg')) is not None
    assert re.fullmatch(r'%s\.png' % filename, _picture_path(None, 'a.png')) is not None

    with pytest.raises(RuntimeError):
        _picture_path(None, 'a.txt')
