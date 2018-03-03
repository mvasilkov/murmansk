from pathlib import Path, PurePath
from string import ascii_letters, digits
import tarfile
from tempfile import TemporaryDirectory

SAFE_CHARACTERS = frozenset(ascii_letters + digits)


def recompress_tar(path: Path, **kwargs) -> Path:
    assert path.suffix == '.tar'
    tar = tarfile.open(path)

    for name in tar.getnames():
        p = PurePath(name).with_suffix('')
        assert set(p.as_posix()).issubset(SAFE_CHARACTERS)

    with TemporaryDirectory(prefix=path.name) as tempdir:
        tempdir = Path(tempdir)
        tar.extractall(tempdir)

        outpath = path.with_suffix('.tar.xz')
        with tarfile.open(outpath, 'x:xz', **kwargs) as outfile:
            for name in tar.getnames():
                outfile.add(tempdir / name, arcname=name)

    tar.close()
    return outpath
