from django import template
from datetime import date, timedelta
import Core.utilityHelper as helper

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

@register.filter(name='get_price_string')
def get_price_string(phone):
    return phone.getPriceString()

@register.filter(name='remove_space')
def remove_space(data):
    return ''.join(e for e in data if e.isalnum())

@register.filter(name='convert_localtime')
def convert_localtime(data):
    return helper.utcToLocal(data).strftime("%d %b %Y %H:%M:%S")