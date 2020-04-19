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