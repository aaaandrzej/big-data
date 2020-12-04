import pandas as pd

from app.bl.exc import FileFormatError
from app.core.timer import timer


@timer
def csv_loader(file, input_fieldnames, usecols):
    df = pd.read_csv(file, delimiter='\t', names=input_fieldnames, usecols=usecols)
    return df


@timer
def filter_positive_population_cities(df):
    df = df[(df.population > 0) & (df.featureclass == 'P')]
    return df


@timer
def update_df_with_country(df, cc_decoder):
    df.insert(3, column='country', value=df['countrycode'].map(cc_decoder))
    return df


@timer
def save_df(df, file, columns):
    file_format = None
    if len(file.rsplit('.')) > 1:
        file_format = file.rsplit('.')[-1]

    if file_format == 'csv':
        df.to_csv(file, columns=columns, index=True)

    elif file_format == 'feather':
        df = df[columns]
        df.reset_index(inplace=True)
        df.to_feather(file)

    else:
        raise FileFormatError

    return
