import os

INPUT_FIELDNAMES = ['geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude', 'featureclass',
                    'featurecode', 'countrycode', 'cc2', 'admin1code', 'admin2code', 'admin3code', 'admin4code',
                    'population', 'elevation', 'dem', 'timezone', 'modificationdate']

INTERIM_FIELDNAMES = ['geonameid', 'name', 'asciiname', 'countrycode', 'latitude', 'longitude', 'featureclass',
                      'population']

OUTPUT_FIELDNAMES = ['geonameid', 'name', 'asciiname', 'country', 'latitude', 'longitude', 'airport']

CC_FIELDNAMES = ['ISO',
                 'ISO3',
                 'ISO-Numeric',
                 'fips',
                 'Country',
                 'Capital',
                 'Area(in sq km)',
                 'Population',
                 'Continent',
                 'tld',
                 'CurrencyCode',
                 'CurrencyName',
                 'Phone',
                 'Postal Code Format',
                 'Postal Code Regex',
                 'Languages',
                 'geonameid',
                 'neighbours',
                 'EquivalentFipsCode']

CC_FIELDNAMES_TRIMMED = ['ISO', 'Country', 'Capital']

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_DIR = 'input-data'
INPUT_FILE_NAME = 'allCountries.txt'

OUTPUT_DIR = 'output-data'
OUTPUT_FILE_NAME = 'allCountries.csv'

INPUT_FILE = os.path.join(ROOT_DIR, INPUT_DIR, INPUT_FILE_NAME)
OUTPUT_FILE = os.path.join(ROOT_DIR, OUTPUT_DIR, OUTPUT_FILE_NAME)

CC_FILE_NAME = '../input-data/countryInfo.txt'
CC_FILE = os.path.join(ROOT_DIR, INPUT_DIR, CC_FILE_NAME)

AIRPORTS_FILE_NAME = 'airports.csv'
AIRPORTS_FILE = os.path.join(ROOT_DIR, INPUT_DIR, AIRPORTS_FILE_NAME)
