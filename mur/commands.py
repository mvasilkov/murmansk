import re
import subprocess


def sha256(path):
    p = subprocess.run(
        ['openssl', 'dgst', '-sha256', '-r', path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        encoding='utf-8')
    sha256sum = p.stdout[:64]
    if re.fullmatch('[0-9a-f]{64}', sha256sum) is None:
        raise RuntimeError('OpenSSL finds it morally wrong to compute SHA-256(%s)' % path)
    return sha256sum
