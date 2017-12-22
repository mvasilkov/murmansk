from datetime import datetime, timezone
import re
from subprocess import check_output
import sys

import django
import mmh3
from mongo.objectid import ObjectId
from mur.commands import sha256
from mur.commonmark import commonmark, version as cmark_version
import requests


def test_python3():
    assert sys.version_info.major == 3 and sys.version_info.minor >= 6


def test_objectid():
    objectid = ObjectId()
    t = datetime.now(timezone.utc)
    assert re.fullmatch('[a-f0-9]{24}', str(objectid))
    assert (t - objectid.generation_time).total_seconds() < 2


def test_commonmark():
    version = cmark_version()
    assert version.major == 0 and version.minor >= 28
    assert commonmark('# heading') == '<h1>heading</h1>\n'


def test_openssl():
    version = check_output(['openssl', 'version'], encoding='utf-8')
    assert version.startswith('OpenSSL 1.0')
    assert (sha256(__file__.replace('test_requirements.py', 'utf-8.txt')) ==
            '4e879c5c63684e8f23998c3a170cc1c5f789808a6ffaf4cef5fd7ab2a4d1bc81')


def test_django(live_server):
    assert django.VERSION[0] == 2
    r = requests.get(
        str(live_server) + '/static/node_modules/systematize/build/systematize.css')
    assert r.status_code == 200
    assert r.text.startswith('/*! systematize.scss | MIT License')


def test_murmurhash3():
    assert mmh3.hash('-Infinity') == -1167832603
    assert mmh3.hash('-Infinity', signed=False) == 3127134693
