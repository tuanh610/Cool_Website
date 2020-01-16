from django import template
from datetime import date, timedelta

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='get_slice')
def get_slice(arr, start, end):
    if start < 0 or end > len(arr) or start < end:
        return []
    else:
        return arr[start:end]
