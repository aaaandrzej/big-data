from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import partial
import math
from typing import Iterable

import pandas as pd

from app.adapters.dynamo_db import save_df_to_dynamodb
from app.adapters.load_csv import load_csv
from app.adapters.save_df import save_df
from app.bl.airport_matching import assign_nearest_airports, assign_nearest_airports_timed
from app.bl.df_manipulations import filter_positive_population_cities, update_df_with_country
from app.core.timer import timer
from app.config import INPUT_FILE, OUTPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES, OUTPUT_FIELDNAMES, \
    AIRPORTS_FILE, CC_FILE, CC_FIELDNAMES, CC_FIELDNAMES_TRIMMED, OPTIMIZATION, \
    LINES_TO_READ, LINES_TO_PROCESS, INPUT_DIR, S3_SOURCE, S3_DESTINATION


def df_chunking_alt(df: pd.DataFrame, chunksize: int) -> Iterable[pd.DataFrame]:
    # TODO add error handling for empty df - ValueError: range() arg 3 must not be zero
    return (df[i:i + chunksize] for i in range(0, df.shape[0], chunksize))


@timer
def func(df, airports, executor_method=None):
    selected_executor = {  # TODO shall executors be initialized in a dict or when used?
        'processes': ProcessPoolExecutor(),
        'threads': ThreadPoolExecutor()  # TODO debug pandas warning raised when using ThreadPoolExecutor()
    }

    if executor_method in selected_executor:

        chunksize = math.ceil(len(df) / 5)

        pd.options.mode.chained_assignment = None  # silent multithreading pandas SettingWithCopyWarning

        with selected_executor[executor_method] as executor:
            chunks_modified = executor.map(partial(assign_nearest_airports, airports=airports),
                                           df_chunking_alt(df, chunksize))

        return pd.concat(chunks_modified)

    else:
        # return map(partial(assign_nearest_airports, airports=airports), df)  # TODO refactor so it works as executor
        return partial(assign_nearest_airports, airports=airports)(df)


def import_cities():
    return partial(load_csv,
                   file_name=INPUT_FILE,
                   input_fieldnames=INPUT_FIELDNAMES,
                   usecols=INTERIM_FIELDNAMES,
                   nrows=LINES_TO_READ,
                   bucket_name=INPUT_DIR,
                   s3=S3_SOURCE)()


def import_airports():
    return partial(load_csv,
                   file_name=AIRPORTS_FILE,
                   delimiter=',',
                   bucket_name=INPUT_DIR,
                   s3=S3_SOURCE)()


def import_cc_codes():
    return partial(load_csv,
                   file_name=CC_FILE,
                   input_fieldnames=CC_FIELDNAMES,
                   usecols=CC_FIELDNAMES_TRIMMED,
                   skiprows=50,
                   bucket_name=INPUT_DIR,
                   s3=S3_SOURCE)()


def cc_codes_processor(source, country_info):  # TODO this is kind of part of BL but minimal and maybe can stay there?
    df = filter_positive_population_cities(source)
    df = update_df_with_country(df, country_info)
    df = df.sort_values('population', ascending=False).head(LINES_TO_PROCESS)
    return df


def airport_matching_processor(source, airports):
    return partial(func, df=source, airports=airports, executor_method=OPTIMIZATION)()


def result_to_file_saver(source):
    return partial(save_df, df=source, file=OUTPUT_FILE, columns=OUTPUT_FIELDNAMES, s3=S3_DESTINATION)()


def result_to_dynamodb_saver(source):
    return partial(save_df_to_dynamodb, df=source, output_fieldnames=OUTPUT_FIELDNAMES)()


def result_to_file_and_dynamodb_saver(source):
    result_to_file_saver(source)
    result_to_dynamodb_saver(source)
