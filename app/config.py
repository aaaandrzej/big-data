import os
from pathlib import Path

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

ENDPOINT_URL = os.getenv('ENDPOINT_URL')

OPTIMIZATION = os.getenv('OPTIMIZATION')
LINES_TO_READ = int(os.getenv('LINES_TO_READ')) if os.getenv('LINES_TO_READ') else None
LINES_TO_PROCESS = int(os.getenv('LINES_TO_PROCESS')) if os.getenv('LINES_TO_PROCESS') else None

if 's3' in os.getenv('INPUT_SOURCE', ''):  # TODO temp workaround, to refactor!! find a way to set up paths source agnostic
    INPUT_DIR = os.getenv('INPUT_DIR')
    INPUT_FILE = os.getenv('INPUT_FILE_NAME')
    CC_FILE = os.getenv('CC_FILE_NAME')
    AIRPORTS_FILE = os.getenv('AIRPORTS_FILE_NAME')

else:
    INPUT_FILE = Path(os.getenv('INPUT_DIR'), os.getenv('INPUT_FILE_NAME'))
    CC_FILE = Path(os.getenv('INPUT_DIR'), os.getenv('CC_FILE_NAME'))
    AIRPORTS_FILE = Path(os.getenv('INPUT_DIR'), os.getenv('AIRPORTS_FILE_NAME'))


OUTPUT_FILE = Path(os.getenv('OUTPUT_DIR'), os.getenv('OUTPUT_FILE_NAME'))


