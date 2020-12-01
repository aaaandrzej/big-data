import os

from app.adapters.all_countries import convert_txt_to_csv_and_update_country_names
from app.adapters.country_codes import cc_decoder
from app.bl.models import City

INPUT_FIELDNAMES = list(City.__dict__['__annotations__'].keys())
OUTPUT_FIELDNAMES = list(City.__dict__['__annotations__'].keys())
OUTPUT_FIELDNAMES.insert(3, 'country')
OUTPUT_FIELDNAMES.remove('alternatenames')

DIR_NAME = '../input-data'
INPUT_FILE_NAME = 'allCountries.txt'
OUTPUT_FILE_NAME = 'allCountries.csv'
INPUT_FILE = os.path.join(DIR_NAME, INPUT_FILE_NAME)
OUTPUT_FILE = os.path.join(DIR_NAME, OUTPUT_FILE_NAME)

CC_FILE = '../input-data/countryInfo.txt'
CC_CODES = cc_decoder(CC_FILE)

if __name__ == '__main__':
    # convert_txt_to_csv_and_update_country_names(input_file=INPUT_FILE, output_file=OUTPUT_FILE,
    #                                     input_fieldnames=INPUT_FIELDNAMES, output_fieldnames=OUTPUT_FIELDNAMES,
    #                                     limit=None, cc_decoder=CC_CODES)
    print(CC_CODES)
    # 12056281 lines written
    # execution time: 0:14:57.239547 [h:mm:ss.milliseconds]