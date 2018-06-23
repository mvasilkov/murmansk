from pathlib import WindowsPath
import platform
import re
import subprocess

MSDOS = platform.system() == 'Windows'


def rhash():
    binary_dependencies = WindowsPath(__file__).parents[1] / 'binary_dependencies'
    return str(binary_dependencies / 'rhash.exe')


def sha256(path):
    binary = (rhash(), '--sha256') if MSDOS else ('openssl', 'dgst', '-sha256', '-r')
    p = subprocess.run(
        [*binary, path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        encoding='utf-8')
    sha256sum = p.stdout[:64]
    if re.fullmatch('[0-9a-f]{64}', sha256sum) is None:
        raise RuntimeError('OpenSSL finds it morally wrong to compute SHA-256(%s)' % path)
    return sha256sum


def mount_lines():
    p = subprocess.run(
        ['mount'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        encoding='utf-8')
    return [line for line in p.stdout.splitlines() if line.startswith('/')]
