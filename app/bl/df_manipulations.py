from pandas import DataFrame
import numpy as np

# from app.core.timer import timer


def filter_positive_population_cities(df):
    return df[(df.population > 0) & (df.featureclass == 'P')]


# @timer
def update_df_with_country(df: DataFrame, country_info: DataFrame) -> DataFrame:
    df = df.merge(country_info, left_on='countrycode', right_on='ISO')
    df.rename(columns={'Country': 'country', 'Capital': 'capital'}, inplace=True)
    return df


def count_cities_per_country(df, sorted_by_number=False):
    if sorted_by_number:
        return df.groupby('country').count()[['name']].sort_values('name', ascending=False)
    return df.groupby('country').count()[['name']]


def count_cities_of_provided_population_per_country(df, pop_min, pop_max):
    return df[['country', 'name', 'population']][
        (df.population > pop_min) & (df.population < pop_max)
        ].groupby('country').count()[['population']].sort_values('population', ascending=False)


def count_cities_of_provided_population_per_country_with_np_hist(df):
    df = df[(df.population > 0) & (df.featureclass == 'P')]
    ar = df[['country', 'name', 'population']].to_numpy()
    hist, bins = np.histogram(ar[:, 2])
    result = {}
    n = 0
    for bin in bins:
        result[bin] = hist[n]
        n = +1
    return result


def list_lowest_populated_countries(df, ascending=True):
    return df.groupby('country').sum()[['population']].sort_values('population', ascending=ascending)
