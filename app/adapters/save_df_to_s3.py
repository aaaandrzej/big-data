import os

import s3fs


def save_df_to_s3(df, filename, columns):
    s3 = s3fs.S3FileSystem(anon=False, client_kwargs={'endpoint_url': os.getenv('ENDPOINT_URL')})

    with s3.open(filename, 'w') as f:
        df.to_csv(f, columns=columns, index=True)

    return
