import pandas as pd

from app.core.timer import timer


@timer
def load_csv(file, input_fieldnames=None, usecols=None, skiprows=None, delimiter='\t', nrows=None):
    df = pd.read_csv(file, delimiter=delimiter, names=input_fieldnames, usecols=usecols, skiprows=skiprows, nrows=nrows)
    return df
