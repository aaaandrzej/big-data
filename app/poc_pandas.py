import pandas as pd
import numpy as np

# from app.adapters.load_airports import airport_loader
from app.adapters.load_csv import load_csv
from app.adapters.save_df import save_df
from app.bl.df_manipulations import filter_positive_population_cities, update_df_with_country
from config import INPUT_FILE, OUTPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES, OUTPUT_FIELDNAMES, \
    AIRPORTS_FILE, CC_FILE, CC_FIELDNAMES, CC_FIELDNAMES_TRIMMED
from app.core.timer import timer

OUTPUT_FILE = OUTPUT_FILE.replace('.csv', '.feather')


@timer
def func():
    country_info = load_csv(CC_FILE, CC_FIELDNAMES, CC_FIELDNAMES_TRIMMED, skiprows=50)
    df = load_csv(INPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES)
    df = filter_positive_population_cities(df)
    df = update_df_with_country(df, country_info)
    save_df(df, OUTPUT_FILE, OUTPUT_FIELDNAMES)
    return df


if __name__ == '__main__':
    df = func()
    # airports = load_csv(AIRPORTS_FILE, delimiter=',')
    #
    # print(airports)
    print(df)
