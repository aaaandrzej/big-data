from geopy.distance import geodesic, great_circle
from pandas import DataFrame

from app.core.timer import timer


# @timer
def find_nearest_airport(latitude: float, longitude: float, airports: DataFrame) -> str:
    point = latitude, longitude
    return airports.loc[airports.apply(lambda x: great_circle(point, (x['lat'], x['lon'])).km, axis=1).idxmin()][
        'ident']


# @timer
def assign_nearest_airports(df: DataFrame, airports: DataFrame) -> DataFrame:
    df['airport'] = df.apply(
        lambda a: find_nearest_airport(latitude=a['latitude'], longitude=a['longitude'], airports=airports
                                       ), axis=1)
    return df


def assign_nearest_airports_timed(df: DataFrame, airports: DataFrame) -> DataFrame:
    return timer(assign_nearest_airports)(df, airports)
