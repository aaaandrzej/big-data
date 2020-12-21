import io
import os

import boto3


def s3_load_file(bucket_name, file_name):
    s3 = boto3.client('s3',
                      endpoint_url=os.getenv('ENDPOINT_URL'),
                      aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

    obj = s3.get_object(Bucket=bucket_name, Key=file_name)

    return io.BytesIO(obj['Body'].read())
