from functools import partial
import multiprocessing as mp

import pandas as pd
import numpy as np
from typing import List

from app.adapters.load_csv import load_csv
from app.adapters.save_df import save_df
from app.bl.airport_matching import assign_nearest_airports
from app.bl.df_manipulations import filter_positive_population_cities, update_df_with_country
from app.core.timer import timer
from config import INPUT_FILE, OUTPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES, OUTPUT_FIELDNAMES, \
    AIRPORTS_FILE, CC_FILE, CC_FIELDNAMES, CC_FIELDNAMES_TRIMMED

OUTPUT_FILE = OUTPUT_FILE.replace('.csv', '.feather')


def df_chunking(df: pd.DataFrame, chunksize: int) -> pd.DataFrame:  # be careful, as it removes all data in initial df
    count = 0
    while len(df):
        count += 1
        yield df.iloc[:chunksize].copy()
        df.drop(df.index[:chunksize], inplace=True)


@timer
def func_no_mp(nrows=None):
    country_info = load_csv(CC_FILE, CC_FIELDNAMES, CC_FIELDNAMES_TRIMMED, skiprows=50)

    df = load_csv(INPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES, nrows=nrows)
    df = filter_positive_population_cities(df)
    df = update_df_with_country(df, country_info)
    df = df.sort_values('population', ascending=False).head(20)

    airports = load_csv(AIRPORTS_FILE, delimiter=',')

    assign_nearest_airports_from_hardcoded_list = partial(assign_nearest_airports, airports=airports)

    assign_nearest_airports_from_hardcoded_list(df)

    return df


@timer
def func_mp(nrows=None):
    country_info = load_csv(CC_FILE, CC_FIELDNAMES, CC_FIELDNAMES_TRIMMED, skiprows=50)

    df = load_csv(INPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES, nrows=nrows)
    df = filter_positive_population_cities(df)
    df = update_df_with_country(df, country_info)
    df = df.sort_values('population', ascending=False).head(20)

    airports = load_csv(AIRPORTS_FILE, delimiter=',')

    n_jobs = 2
    n_chunks = len(df) // n_jobs

    chunks = [chunk for chunk in df_chunking(df, n_chunks)]

    with mp.Pool(n_jobs) as pool:
        chunks_modified = pool.map(partial(assign_nearest_airports, airports=airports), chunks)

    return pd.concat(chunks_modified)


if __name__ == '__main__':
    a = func_no_mp()
    # b = func_mp()

    # df = filter_positive_population_cities(df)

    # df = update_df_with_country(df, country_info)

    # airports = load_csv(AIRPORTS_FILE, delimiter=',')
    #
    # dfa = df.sort_values('population', ascending=False).head(500)
    # dfb = assign_nearest_airports(dfa, airports)
    #
    # save_df(dfb, OUTPUT_FILE, OUTPUT_FIELDNAMES)

    # return
#
# func()

# export PYTHONPATH=.
# python app/poc_pandas.py > perf-logs/perf_log_500cities_1proc_1thread.log
