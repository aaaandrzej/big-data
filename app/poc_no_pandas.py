import csv
from copy import copy
import os

from app.adapters.country_codes import cc_decoder
from app.core.timer import timer


@timer
def convert_txt_to_csv_and_update_country_names(input_file, input_fieldnames,
                                                cc_decoder, delimiter='\t', limit=0):
    counter = 0

    with open(input_file) as input:
        reader = csv.DictReader(input, fieldnames=input_fieldnames, delimiter=delimiter)

        city_list = []

        for row in reader:
            city_as_dict = row

            try:
                city_as_dict['country'] = cc_decoder[city_as_dict['countrycode']]
            except KeyError:
                city_as_dict['country'] = None

            del city_as_dict['alternatenames']
            city_list.append(city_as_dict)
            counter += 1

            if limit != 0 and counter >= limit:
                break

    print(f'\n{counter} lines read\n')
    return city_list


@timer
def write_list_to_csv(content, output_file, output_fieldnames):
    with open(output_file, 'w', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=output_fieldnames)
        writer.writeheader()
        writer.writerows(content)

    print(f'\n{len(content)} lines written\n')
    return


INPUT_FIELDNAMES = ['geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude', 'featureclass',
                    'featurecode', 'countrycode', 'cc2', 'admin1code', 'admin2code', 'admin3code', 'admin4code',
                    'population', 'elevation', 'dem', 'timezone', 'modificationdate']
OUTPUT_FIELDNAMES = copy(INPUT_FIELDNAMES)
OUTPUT_FIELDNAMES.insert(3, 'country')
OUTPUT_FIELDNAMES.remove('alternatenames')

INPUT_DIR_NAME = '../input-data'
INPUT_FILE_NAME = 'allCountries.txt'

OUTPUT_DIR_NAME = '../output-data'
OUTPUT_FILE_NAME = 'allCountries.csv'

INPUT_FILE = os.path.join(INPUT_DIR_NAME, INPUT_FILE_NAME)
OUTPUT_FILE = os.path.join(OUTPUT_DIR_NAME, OUTPUT_FILE_NAME)

CC_FILE = '../input-data/countryInfo.txt'

if __name__ == '__main__':
    CC_CODES = cc_decoder(CC_FILE)

    city_list = convert_txt_to_csv_and_update_country_names(input_file=INPUT_FILE,
                                                            input_fieldnames=INPUT_FIELDNAMES,
                                                            # limit=10,
                                                            cc_decoder=CC_CODES)

    write_list_to_csv(city_list, output_file=OUTPUT_FILE, output_fieldnames=OUTPUT_FIELDNAMES)

    # pass

    # 12056281 lines I/O operations
    #
    # row by row read/write to csv:
    # execution time: 0:14:57.239547 [h:mm:ss.milliseconds]
    #
    # list with 12m dicts read and written to csv in one go:
    # execution time: 0:06:04.887862[h:mm:ss.milliseconds]
