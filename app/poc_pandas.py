import pandas as pd
import numpy as np

from app.adapters.load_csv import load_csv
from app.adapters.save_df import save_df
from app.bl.airport_matching import assign_nearest_airports
from app.bl.df_manipulations import filter_positive_population_cities, update_df_with_country
from config import INPUT_FILE, OUTPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES, OUTPUT_FIELDNAMES, \
    AIRPORTS_FILE, CC_FILE, CC_FIELDNAMES, CC_FIELDNAMES_TRIMMED

OUTPUT_FILE = OUTPUT_FILE.replace('.csv', '.feather')


if __name__ == '__main__':

    country_info = load_csv(CC_FILE, CC_FIELDNAMES, CC_FIELDNAMES_TRIMMED, skiprows=50)

    df = load_csv(INPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES, nrows=None)
    df = filter_positive_population_cities(df)
    df = update_df_with_country(df, country_info)
    # save_df(df, OUTPUT_FILE, OUTPUT_FIELDNAMES)

    airports = load_csv(AIRPORTS_FILE, delimiter=',')

    dfa = df.sort_values('population', ascending=False).head(10)
    dfb = assign_nearest_airports(dfa, airports)

    print(dfb)

    # for 50 records:
    # assign_nearest_airports function execution time: 0:05:14.024787 [h:mm:ss.milliseconds]
    # for 10 records:
    # assign_nearest_airports function execution time: 0:01:09.025166 [h:mm:ss.milliseconds]
