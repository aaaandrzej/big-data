# - dostanę listę lotnisk
# - znaleźć sposób i bibliotekę mierzenia odległości (pewnie model great circle, geopy, ew. scipy)
# - wybrać listę miejscowości (np stolice) i dopasować najbliższe lotnisko

import geopy.distance
from pandas import DataFrame, pandas as pd

from app.adapters.load_csv import load_csv
from app.core.timer import timer
from config import AIRPORTS_FILE


@timer
def find_nearest_airport(latitude: float, longitude: float, airports: DataFrame) -> str:
    point = latitude, longitude
    airports['dist'] = airports.apply(lambda x: geopy.distance.distance(point, (x['lat'], x['lon'])), axis=1)
    return airports.sort_values('dist')['ident'].values[0]


def assign_nearest_airports(df: DataFrame, airports: DataFrame) -> DataFrame:


    return


if __name__ == '__main__':

    airports = load_csv(AIRPORTS_FILE, delimiter=',')

    print(find_nearest_airport(54.3520, 18.6466, airports))
    print(find_nearest_airport(54.377498626708984, 18.466110229492188, airports))
