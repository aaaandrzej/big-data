import pandas as pd
import numpy as np

from app.adapters.load_csv import csv_loader
from app.adapters.save_df import save_df
from app.bl.df_manipulations import filter_positive_population_cities, update_df_with_country
from config import CC_CODES, INPUT_FILE, OUTPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES, OUTPUT_FIELDNAMES
from app.core.timer import timer

OUTPUT_FILE = OUTPUT_FILE.replace('.csv', '.feather')


@timer
def func():
    df = csv_loader(INPUT_FILE, INPUT_FIELDNAMES, INTERIM_FIELDNAMES)
    df = filter_positive_population_cities(df)
    df = update_df_with_country(df, CC_CODES)
    save_df(df, OUTPUT_FILE, OUTPUT_FIELDNAMES)
    return df


if __name__ == '__main__':

    df = func()



# csv whole file manipulation
# csv_loader function execution time: 0:01:01.408433 [h:mm:ss.milliseconds]
# update_df_with_country_and_trim_alternatenames function execution time: 0:00:07.336487 [h:mm:ss.milliseconds]
# save_df function execution time: 0:02:26.645463 [h:mm:ss.milliseconds]
# convert function execution time: 0:03:39.487629 [h:mm:ss.milliseconds]

# csv trimmed file manipulation
# csv_loader function execution time: 0:00:26.976383 [h:mm:ss.milliseconds]
# filter_positive_population_cities function execution time: 0:00:01.512686 [h:mm:ss.milliseconds]
# update_df_with_country function execution time: 0:00:00.117338 [h:mm:ss.milliseconds]
# save_df function execution time: 0:00:03.498150 [h:mm:ss.milliseconds]
# convert function execution time: 0:00:32.981207 [h:mm:ss.milliseconds]

# feather trimmed file manipulation
# csv_loader function execution time: 0:00:23.110976 [h:mm:ss.milliseconds]
# filter_positive_population_cities function execution time: 0:00:00.871699 [h:mm:ss.milliseconds]
# update_df_with_country function execution time: 0:00:00.064459 [h:mm:ss.milliseconds]
# save_df function execution time: 0:00:00.363873 [h:mm:ss.milliseconds]
# convert function execution time: 0:00:25.174638 [h:mm:ss.milliseconds]
