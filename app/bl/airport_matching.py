import geopy.distance
from pandas import DataFrame

from app.core.timer import timer


@timer
def find_nearest_airport(latitude: float, longitude: float, airports: DataFrame) -> str:
    point = latitude, longitude
    airports['dist'] = airports.apply(lambda x: geopy.distance.distance(point, (x['lat'], x['lon'])), axis=1)
    return airports[airports.dist == airports['dist'].min()]['ident'].values[0]


@timer
def assign_nearest_airports(df: DataFrame, airports: DataFrame) -> DataFrame:
    df['airport'] = df.apply(
        lambda a: find_nearest_airport(latitude=a['latitude'], longitude=a['longitude'], airports=airports
                                       ), axis=1)
    return df
