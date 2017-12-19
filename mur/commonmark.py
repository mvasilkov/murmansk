from collections import namedtuple
from ctypes import CDLL, c_char_p, c_size_t, c_int
import platform

if platform.system() == 'Darwin':
    cmark = CDLL('libcmark.dylib')
else:
    cmark = CDLL('libcmark.so')

cmark_markdown_to_html = cmark.cmark_markdown_to_html
cmark_markdown_to_html.argtypes = (c_char_p, c_size_t, c_int)
cmark_markdown_to_html.restype = c_char_p

cmark_version = cmark.cmark_version
cmark_version.restype = c_int

VT = namedtuple('VT', 'major minor patchlevel')


def commonmark(string):
    b = string.encode('utf-8')
    return cmark_markdown_to_html(b, len(b), 0).decode('utf-8')


def version():
    return VT(*cmark_version().to_bytes(3, byteorder='big'))
