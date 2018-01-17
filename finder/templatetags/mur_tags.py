from django import template
from django.utils.safestring import mark_safe

from mur.commonmark import commonmark

register = template.Library()


@register.filter(name='commonmark')
def commonmark_filter(string):
    return mark_safe(commonmark(string)) if string else ''


@register.filter(name='classname')
def classname_filter(instance):
    return instance.__class__.__name__
