import os
from io import StringIO

import boto3


def s3_save_df(df, filename, columns):
    s3 = boto3.resource('s3',
                        endpoint_url=os.getenv('ENDPOINT_URL'),
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, columns=columns, index=True)
    s3.Object(f'{filename.parent}', f'{filename.name}').put(Body=csv_buffer.getvalue())  # TODO is f' OK here?
