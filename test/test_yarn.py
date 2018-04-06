from yarn.finders import YarnFinder

from os.path import isfile, join as joinpath
from pathlib import PurePath


def clean_yarn_settings(settings):
    del settings.YARN_ALLOW_FILES
    del settings.YARN_ROOT_PATH
    del settings.YARN_STATIC_FILES_PREFIX
    # django-npm compatibility
    del settings.NPM_ROOT_PATH
    del settings.NPM_STATIC_FILES_PREFIX


def count(gen):
    return sum(1 for _ in gen)


def test_yarn_finder(settings):
    systematize = 'systematize/build/systematize.css'
    syspath = settings.DJANGO_ROOT / 'node_modules' / systematize
    assert isfile(syspath)

    clean_yarn_settings(settings)

    findpath = joinpath('yarn-testing', systematize)
    finder = YarnFinder()
    assert not finder.find(findpath)

    settings.YARN_ROOT_PATH = settings.DJANGO_ROOT.as_posix()
    settings.YARN_STATIC_FILES_PREFIX = 'yarn-testing'

    finder = YarnFinder()
    assert syspath.samefile(finder.find(findpath))

    clean_yarn_settings(settings)
    settings.NPM_ROOT_PATH = settings.DJANGO_ROOT.as_posix()
    settings.NPM_STATIC_FILES_PREFIX = 'yarn-testing'

    finder = YarnFinder()
    assert syspath.samefile(finder.find(findpath))


def test_yarn_allow_files(settings):
    systematize = 'systematize/build/systematize.css'
    syspath = settings.DJANGO_ROOT / 'node_modules' / systematize
    assert isfile(syspath)
    assert isfile(syspath.with_suffix('.min.css'))

    clean_yarn_settings(settings)
    settings.YARN_ALLOW_FILES = None
    settings.YARN_ROOT_PATH = settings.DJANGO_ROOT.as_posix()
    settings.YARN_STATIC_FILES_PREFIX = 'yarn-testing'

    findpath = joinpath('yarn-testing', systematize)
    finder = YarnFinder()
    assert not finder.find(findpath)
    assert not list(finder.list(None))

    settings.YARN_ALLOW_FILES = [systematize]

    finder = YarnFinder()
    assert syspath.samefile(finder.find(findpath))
    # PurePath is needed because Windows
    assert [PurePath(a) for a, b in finder.list(None)] == [PurePath(systematize)]

    settings.YARN_ALLOW_FILES = ['systematize/build/*.css']

    finder = YarnFinder()
    assert count(finder.list(None)) == 2
