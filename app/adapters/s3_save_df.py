import os
from io import StringIO

import boto3


# import s3fs  # TODO pick either s3fs or boto3 to ensure consistency  # TODO consider dropping s3fs as causes conflicts

# from app.core.timer import timer


# @timer
# def s3_save_df(df, filename, columns):
#     s3 = s3fs.S3FileSystem(anon=False, client_kwargs={'endpoint_url': os.getenv('ENDPOINT_URL')})
#
#     with s3.open(filename, 'w') as f:
#         df.to_csv(f, columns=columns, index=True)
#
#     return


def s3_save_df(df, filename, columns):
    s3 = boto3.resource('s3',
                        endpoint_url=os.getenv('ENDPOINT_URL'),
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, columns=columns, index=True)
    s3.Object(f'{filename.parent}', f'{filename.name}').put(Body=csv_buffer.getvalue())  # TODO is f' OK here?
