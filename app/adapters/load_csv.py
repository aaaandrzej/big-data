import pandas as pd

from app.core.timer import timer


@timer
def csv_loader(file, input_fieldnames, usecols):
    df = pd.read_csv(file, delimiter='\t', names=input_fieldnames, usecols=usecols)
    return df
