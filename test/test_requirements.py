import re
import sys

from mongo.objectid import ObjectId


def test_python3():
    assert sys.version_info.major == 3 and sys.version_info.minor >= 6


def test_objectid():
    assert re.fullmatch('[a-z0-9]{24}', str(ObjectId()))
