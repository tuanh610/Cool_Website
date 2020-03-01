import logging
import boto3
from botocore.exceptions import ClientError

def upload_file(file_name, bucket, object_name=None):
    """
    Upload a file to S3 bucket
    :param file_name: name of file to upload
    :param bucket: bucket to upload to
    :param object_name: S3 object name. iF not specified then file_name will be used
    :return: True if file is uploaded, else false
    """

    #If object_name is not defined then use file_name
    if object_name is None:
        object_name = file_name
    #If object_name is a path name, then only takes the last part of the name
    if object_name.find('\\') != -1:
        object_name = object_name.split('\\')[-1]


    #Upload file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True