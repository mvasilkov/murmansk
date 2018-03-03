import os
from pathlib import Path
import tarfile

from mur.archiver import recompress_tar

genbytes_tab = bytes.maketrans(bytearray(range(256)),
                               bytearray([ord(b'a') + b % 26 for b in range(256)]))


def genbytes(size: int = 2 ** 20):
    return os.urandom(size).translate(genbytes_tab)


def cleanup(*args: str):
    for a in args:
        try:
            os.remove(a)
        except FileNotFoundError:
            pass


def test_recompress_ratio():
    contents = genbytes()

    with open('ab.txt', 'wb') as outfile:
        outfile.write(contents)
    with tarfile.open('ab.tar', 'w') as outfile2:
        outfile2.add('ab.txt')
    size = os.stat('ab.tar').st_size

    try:
        outpath = recompress_tar(Path('ab.tar'), preset=0)
        size1 = outpath.stat().st_size
        cleanup(outpath.as_posix())

        outpath = recompress_tar(Path('ab.tar'), preset=9)
        size2 = outpath.stat().st_size
        assert size > size1 > size2
    finally:
        cleanup('ab.txt', 'ab.tar', 'ab.tar.xz')
