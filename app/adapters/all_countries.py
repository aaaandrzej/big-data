import csv

from app.bl.models import City
from app.core.timer import timer


@timer
def convert_txt_to_csv_and_update_country_names(input_file, output_file, input_fieldnames, output_fieldnames, cc_decoder,
                                        delimiter='	', limit=None):
    counter = 0

    with open(input_file) as input, open(output_file, 'w', newline='') as output:

        reader = csv.DictReader(input, fieldnames=input_fieldnames, delimiter=delimiter)

        writer = csv.DictWriter(output, fieldnames=output_fieldnames)

        writer.writeheader()

        for row in reader:
            city_as_dict = City(**row).object_as_dict()

            try:
                city_as_dict['country'] = cc_decoder[city_as_dict['countrycode']]
            except KeyError:
                city_as_dict['country'] = None

            del city_as_dict['alternatenames']
            writer.writerow(city_as_dict)
            counter += 1

            if limit is not None and counter >= limit:
                break

    stats = f'\n{counter} lines written\n'
    print(stats)
    return
