from collections import namedtuple
from ctypes import CDLL, c_char_p, c_size_t, c_int

cmark = CDLL('libcmark.dylib')

cmark_markdown_to_html = cmark.cmark_markdown_to_html
cmark_markdown_to_html.argtypes = (c_char_p, c_size_t, c_int)
cmark_markdown_to_html.restype = c_char_p

cmark_version = cmark.cmark_version
cmark_version.restype = c_int

VT = namedtuple('VT', 'major minor patchlevel')


def commonmark(string):
    bytestring = string.encode('utf-8')
    length = len(bytestring)
    return cmark_markdown_to_html(bytestring, length, 0).decode('utf-8')


def version():
    return VT(*cmark_version().to_bytes(3, byteorder='big'))
