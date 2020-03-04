from django import template
from datetime import date, timedelta
import Core.utilityHelper as helper
from Core.constant import s3_bucket_name
import boto3
from botocore.errorfactory import ClientError

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


@register.filter(name='get_thumbnail')
def get_thumbnail(link, size):
    #Link: https://s3.ap-southeast-1.amazonaws.com/imagestore.tuanh1234/media/images/pennies.jpg?AWSAccessKeyId=AKIA2ILY674A2I4VGCV5&Signature=TbNqBQRGjkuMgujPDQcL3Oo5ujQ%3D&Expires=1583306819
    #strip off the access key first
    obj_name = None
    try:
        idx = link.find('?')
        actual_link = link[:idx]
        idx = actual_link.find(s3_bucket_name) + len(s3_bucket_name) + 1
        obj_name = actual_link[idx:]
        if "/" in obj_name:
            idx = obj_name.rfind('/')
            obj_name = "{path}/{size}_{name}".format(path=obj_name[:idx], size=size, name=obj_name[idx+1:])
        else:
            obj_name = "{size}_{name}".format(size=size, name=obj_name)
        if helper.check_file_exist_s3(s3_bucket_name, obj_name):
            presigned_link = helper.create_presigned_url(s3_bucket_name, obj_name)
            return presigned_link
        else:
            return helper.create_lambda_link(obj_name)
    except ClientError as e:
        if obj_name is not None:
            return helper.create_lambda_link(obj_name)
        else:
            return None