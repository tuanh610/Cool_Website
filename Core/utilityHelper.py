import Core.scraping.PhoneData as PhoneData
import Core.database.phoneDBEngine as phoneDBEngine
import Core.constant as constant
import pathlib
from datetime import datetime, timezone
import boto3
from botocore.exceptions import ClientError
import logging
import Core.constant as constants


def utcToLocal(utc_dt:datetime):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def arrangePhonesToList(phones: [PhoneData]):
    data = {}
    for phone in phones:
        if phone.getName() in data:
            data[phone.getName()].append(phone)
        else:
            data[phone.getName()] = [phone]
    return data


def getLowestPriceList(phones: [PhoneData]):
    data = {}
    for phone in phones:
        if phone.getName() not in data or phone.getPrice() < data[phone.getName()].getPrice():
            data[phone.getName()] = phone
    return data


def initBrandsUsingTextFile():
    phoneDBAdaper = phoneDBEngine(constant.dynamoDBTableName)
    f = open("brands.txt", "r")
    content = f.read()
    f.close()
    brands = content.split(',')
    map(lambda x: x.strip(), brands)
    phoneDBAdaper.updateAllBrandData(brands)


def readBrandsFromFile():
    fileName = str(pathlib.Path(__file__).parent.absolute()) + "/brands.txt"
    f = open(fileName, "r")
    content = f.read()
    f.close()
    brands = content.split(',')
    return [item.strip() for item in brands]

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """
    Generate a presigned URL to share S3 object
    :param bucket_name: name of bucket
    :param object_name: name of object
    :param expiration: expiration time in seconds
    :return: presigned url
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={
                                                        'Bucket': bucket_name,
                                                        'Key': object_name
                                                    },
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return response

def create_lambda_link(object_name):
    return constants.lambda_endpoint + object_name

def check_file_exist_s3(bucket_name, object_name):
    try:
        s3 = boto3.resource('s3')
        s3.Object(bucket_name, object_name).load()
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            logging.error(e)
            return False
    else:
        return True
