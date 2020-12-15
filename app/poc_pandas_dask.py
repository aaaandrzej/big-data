import pandas as pd
import numpy as np
import dask.dataframe as dd

from app.adapters.load_csv import load_csv
from app.adapters.save_df import save_df
from app.bl.airport_matching import assign_nearest_airports
from app.bl.df_manipulations import filter_positive_population_cities, update_df_with_country
from app.core.timer import timer
from config import INPUT_FILE, OUTPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES, OUTPUT_FIELDNAMES, \
    AIRPORTS_FILE, CC_FILE, CC_FIELDNAMES, CC_FIELDNAMES_TRIMMED

OUTPUT_FILE = OUTPUT_FILE.replace('.csv', '.feather')

if __name__ == '__main__':
    # @timer
    # def func():

    country_info = load_csv(CC_FILE, CC_FIELDNAMES, CC_FIELDNAMES_TRIMMED, skiprows=50)

    df = load_csv(INPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES, nrows=None)
    # df = dd.read_csv(INPUT_FILE, names=INPUT_FIELDNAMES, columns=INTERIM_FIELDNAMES, blocksize=128 * 1024 * 1024)
    df = filter_positive_population_cities(df)
    df = update_df_with_country(df, country_info)

    airports = load_csv(AIRPORTS_FILE, delimiter=',')

    dfa = df.sort_values('population', ascending=False).head(500)
    dfd = dd.from_pandas(dfa, npartitions=4)

    dfdd = assign_nearest_airports(dfd, airports)  # exectuion startin there, which is too early..
    # in fact above seems to be an infinite loop - to be rewritten definitely
    dfdd.compute(num_workers=2)  # ?? # didnt get there

    #
    # save_df(dfb, OUTPUT_FILE, OUTPUT_FIELDNAMES)

    # return
#
# func()

# export PYTHONPATH=.
# python app/poc_pandas.py > perf-logs/perf_log_500cities_1proc_1thread.log
