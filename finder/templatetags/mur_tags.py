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


@register.filter(name='equals')
def equals_filter(model, another_model):
    return model.id == another_model.id if another_model else False
