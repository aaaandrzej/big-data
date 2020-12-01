import pandas as pd
import numpy as np
import os

from app.adapters.country_codes import cc_decoder
from app.bl.models import City
from app.core.timer import timer

INPUT_FIELDNAMES = list(City.__dict__['__annotations__'].keys())
OUTPUT_FIELDNAMES = list(City.__dict__['__annotations__'].keys())
OUTPUT_FIELDNAMES.insert(3, 'country')
OUTPUT_FIELDNAMES.remove('alternatenames')

DIR_NAME = '../input-data'
INPUT_FILE_NAME = 'allCountries.txt'
OUTPUT_FILE_NAME = 'allCountries.csv'
INPUT_FILE = os.path.join(DIR_NAME, INPUT_FILE_NAME)
OUTPUT_FILE = os.path.join(DIR_NAME, OUTPUT_FILE_NAME)

CC_FILE = '../input-data/countryInfo.txt'
CC_CODES = cc_decoder(CC_FILE)


# @timer
# def pandas_read_csv(file, delimiter):
#     df = pd.read_csv(file, delimiter=delimiter)
#     print(type(df))
#     print(df.info())
#     print()
#     return df


if __name__ == '__main__':

    df = pd.read_csv(INPUT_FILE, delimiter='	', names=INPUT_FIELDNAMES, usecols=[1,2,3])
    df_trimmed = df.drop(columns=['alternatenames'])

    df = pd.read_csv(INPUT_FILE, delimiter='	', names=INPUT_FIELDNAMES,
                     usecols=['name', 'asciiname', 'countrycode', 'latitude', 'longitude', 'population'])


    # df = pandas_read_csv(INPUT_FILE, delimiter='	')
    # result = pd.unique(df['Item Type'])
    # result = df['Region'].value_counts()
    # result = df.loc[2, 'Region']
    print(df)
    # print(type(df))
    print(df.info())
