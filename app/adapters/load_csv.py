import pandas as pd

from app.adapters.s3_load_file import s3_load_file
# from app.core.timer import timer


# @timer
def load_csv(file_name, input_fieldnames=None, usecols=None, skiprows=None, delimiter='\t', nrows=None,
             bucket_name=None, s3=False):
    file = file_name
    if s3:
        file = s3_load_file(bucket_name, file_name)

    df = pd.read_csv(file, delimiter=delimiter, names=input_fieldnames, usecols=usecols, skiprows=skiprows, nrows=nrows,
                     keep_default_na=False)
    return df
