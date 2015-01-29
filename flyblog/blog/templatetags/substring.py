# coding:utf-8

from django import template

register = template.Library()
# pagedivider


@register.filter(name='sub')
def sub(value, param):
    if not value:
        return value
    try:
        value = int(value)
        param = int(param)
    except TypeError:
        return value
    return value - param
