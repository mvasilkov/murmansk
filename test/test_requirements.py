import re
import sys

from mongo.objectid import ObjectId
from mur.commonmark import commonmark, version as cmark_version


def test_python3():
    assert sys.version_info.major == 3 and sys.version_info.minor >= 6


def test_objectid():
    assert re.fullmatch('[a-z0-9]{24}', str(ObjectId()))


def test_commonmark():
    version = cmark_version()
    assert version.major == 0 and version.minor >= 28
    assert commonmark('# heading') == '<h1>heading</h1>\n'
