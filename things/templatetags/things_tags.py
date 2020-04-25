from django.template.defaultfilters import stringfilter
from django.utils.safestring import SafeData, mark_safe
from django import template

register = template.Library()


@register.filter
@stringfilter
def thing_time(value):
    if not value:
        return
    safe = isinstance(value, SafeData)
    if safe:
        value = int(value)
        return mark_safe(value)
    return value


@register.filter
@stringfilter
def int_time(value):
    if not value:
        return ''
    try:
        int_value = int(value)
        total_sec = int_value // 1000
        milisec = int_value % 1000
        total_min = total_sec // 60
        sec = total_sec % 60
        hour = total_min // 60
        min = total_min % 60
        return "{}:{}:{}.{}".format(hour, str(min).zfill(2), str(sec).zfill(2), str(milisec).zfill(3))
    except ValueError as e:
        return value
