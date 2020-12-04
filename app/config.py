import os

from app.adapters.country_codes import cc_decoder

INPUT_FIELDNAMES = ['geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude', 'featureclass',
                    'featurecode', 'countrycode', 'cc2', 'admin1code', 'admin2code', 'admin3code', 'admin4code',
                    'population', 'elevation', 'dem', 'timezone', 'modificationdate']

INTERIM_FIELDNAMES = ['geonameid', 'name', 'asciiname', 'countrycode', 'latitude', 'longitude', 'featureclass',
                      'population']

OUTPUT_FIELDNAMES = ['geonameid', 'name', 'asciiname', 'country', 'latitude', 'longitude']

INPUT_DIR_NAME = '../input-data'
INPUT_FILE_NAME = 'allCountries.txt'

OUTPUT_DIR_NAME = '../output-data'
OUTPUT_FILE_NAME = 'allCountries.csv'

INPUT_FILE = os.path.join(INPUT_DIR_NAME, INPUT_FILE_NAME)
OUTPUT_FILE = os.path.join(OUTPUT_DIR_NAME, OUTPUT_FILE_NAME)

CC_FILE = '../input-data/countryInfo.txt'
CC_CODES = cc_decoder(CC_FILE)
