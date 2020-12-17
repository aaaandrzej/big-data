from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import partial
import math
from typing import Iterable

import pandas as pd

from app.adapters.load_csv import load_csv
from app.adapters.save_df import save_df
from app.bl.airport_matching import assign_nearest_airports, assign_nearest_airports_timed
from app.bl.df_manipulations import filter_positive_population_cities, update_df_with_country
from app.core.timer import timer
from app.config import INPUT_FILE, OUTPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES, OUTPUT_FIELDNAMES, \
    AIRPORTS_FILE, CC_FILE, CC_FIELDNAMES, CC_FIELDNAMES_TRIMMED

OUTPUT_FILE = str(OUTPUT_FILE).replace('.csv', '.feather')


def df_chunking_alt(df: pd.DataFrame, chunksize: int) -> Iterable[pd.DataFrame]:
    return (df[i:i + chunksize] for i in range(0, df.shape[0], chunksize))


@timer
def func(df, airports, executor_method=None):

    selected_executor = {  # TODO shall executors be initialized in a dict or when used?
        'processes': ProcessPoolExecutor(),
        'threads': ThreadPoolExecutor()  # TODO debug pandas warning raised when using ThreadPoolExecutor()
    }

    if executor_method in selected_executor:

        chunksize = math.ceil(len(df) / 5)

        with selected_executor[executor_method] as executor:
            chunks_modified = executor.map(partial(assign_nearest_airports, airports=airports),
                                           df_chunking_alt(df, chunksize))

        return pd.concat(chunks_modified)

    else:
        # return map(partial(assign_nearest_airports, airports=airports), df)  # TODO refactor so it works as executor
        return partial(assign_nearest_airports, airports=airports)(df)


if __name__ == '__main__':
    country_info = load_csv(CC_FILE, CC_FIELDNAMES, CC_FIELDNAMES_TRIMMED, skiprows=50)
    df = load_csv(INPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES, nrows=10000)
    df = filter_positive_population_cities(df)
    df = update_df_with_country(df, country_info)
    df = df.sort_values('population', ascending=False).head(5)
    airports = load_csv(AIRPORTS_FILE, delimiter=',')
    # print('prep done')

    a = func(df, airports)
    b = func(df, airports, executor_method='processes')
    c = func(df, airports, executor_method='threads')
    d = func(df, airports, executor_method='unicorns')

    save_df(a, OUTPUT_FILE, OUTPUT_FIELDNAMES)
