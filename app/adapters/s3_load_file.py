import io

import boto3


def s3_load_file(bucket_name, file_name):
    s3 = boto3.client('s3',
                      endpoint_url='http://localhost:4566',  # TODO refactor to use environment variables
                      aws_access_key_id='test',
                      aws_secret_access_key='test')

    obj = s3.get_object(Bucket=bucket_name, Key=file_name)

    return io.BytesIO(obj['Body'].read())
