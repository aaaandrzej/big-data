import math
from functools import partial
import multiprocessing as mp

import pandas as pd
import numpy as np
from typing import List, Generator, Iterable

from app.adapters.load_csv import load_csv
from app.adapters.save_df import save_df
from app.bl.airport_matching import assign_nearest_airports, assign_nearest_airports_timed
from app.bl.df_manipulations import filter_positive_population_cities, update_df_with_country
from app.core.timer import timer
from config import INPUT_FILE, OUTPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES, OUTPUT_FIELDNAMES, \
    AIRPORTS_FILE, CC_FILE, CC_FIELDNAMES, CC_FIELDNAMES_TRIMMED

OUTPUT_FILE = OUTPUT_FILE.replace('.csv', '.feather')


def df_chunking_alt(df: pd.DataFrame, chunksize: int) -> Iterable[pd.DataFrame]:
    return (df[i:i + chunksize] for i in range(0, df.shape[0], chunksize))


@timer
def func(n_jobs=0, input_lines=None, output_lines=20):
    country_info = load_csv(CC_FILE, CC_FIELDNAMES, CC_FIELDNAMES_TRIMMED, skiprows=50)

    df = load_csv(INPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES, nrows=input_lines)
    df = filter_positive_population_cities(df)
    df = update_df_with_country(df, country_info)
    df = df.sort_values('population', ascending=False).head(output_lines)

    airports = load_csv(AIRPORTS_FILE, delimiter=',')

    if n_jobs < 0:
        raise ValueError('n_jobs must be greater or equal 0')

    elif n_jobs > 0:

        chunksize = math.ceil(len(df) / n_jobs)  # TODO experiment with more chunks and measure results

        with mp.Pool(n_jobs) as pool:
            chunks_modified = pool.map(partial(assign_nearest_airports, airports=airports),
                                       df_chunking_alt(df, chunksize))

        return pd.concat(chunks_modified)

    else:
        # return map(partial(assign_nearest_airports, airports=airports), df)
        return partial(assign_nearest_airports, airports=airports)(df)


if __name__ == '__main__':
    a = func(n_jobs=0, input_lines=100000, output_lines=50)
    b = func(n_jobs=4, input_lines=100000, output_lines=50)

    # save_df(dfb, OUTPUT_FILE, OUTPUT_FIELDNAMES)

    # func()

# export PYTHONPATH=.
# python app/poc_pandas.py > perf-logs/perf_log_500cities_1proc_1thread.log
