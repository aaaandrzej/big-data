import csv

from config import OUTPUT_FILE, INPUT_FILE, INPUT_FIELDNAMES, OUTPUT_FIELDNAMES, CC_FILE, CC_FIELDNAMES
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

            city_list.append(city_as_dict)
            counter += 1

            if limit != 0 and counter >= limit:
                break

    print(f'\n{counter} lines read\n')
    return city_list


@timer
def trim_obsolete_columns(content, input_fieldnames, output_fieldnames):
    obsolete_fieldnames = [field for field in input_fieldnames if field not in output_fieldnames]
    for item in content:  # logic potentially to be reduced and moved inside convert function
        for field in obsolete_fieldnames:
            del item[field]  # proven to be 2x faster than item.pop(field)
    return


@timer
def write_list_to_csv(content, output_file, output_fieldnames):
    with open(output_file, 'w', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=output_fieldnames)
        writer.writeheader()
        writer.writerows(content)

    print(f'\n{len(content)} lines written\n')
    return


def cc_decoder(file, fieldnames=CC_FIELDNAMES):
    with open(file) as csv_file:
        for i in range(50):
            csv_file.__next__()
        reader = csv.DictReader(csv_file, delimiter='	', fieldnames=fieldnames)
        cc_decoded = {row['ISO']: row['Country'] for row in reader}
        return cc_decoded


if __name__ == '__main__':
    CC_CODES = cc_decoder(CC_FILE)

    OUTPUT_FIELDNAMES.remove('airport')  # added airports in pandas but out of scope here

    city_list = convert_txt_to_csv_and_update_country_names(input_file=INPUT_FILE,
                                                            input_fieldnames=INPUT_FIELDNAMES,
                                                            limit=10,
                                                            cc_decoder=CC_CODES)

    trim_obsolete_columns(city_list, input_fieldnames=INPUT_FIELDNAMES, output_fieldnames=OUTPUT_FIELDNAMES)

    write_list_to_csv(city_list, output_file=OUTPUT_FILE, output_fieldnames=OUTPUT_FIELDNAMES)

    # pass

    # 12056281 lines I/O operations
    #
    # row by row read/write to csv:
    # execution time: 0:14:57.239547 [h:mm:ss.milliseconds]
    #
    # list with 12m dicts read and written to csv in one go:
    # execution time: 0:06:04.887862[h:mm:ss.milliseconds]
    # execution time: 0:07:25.912101[h:mm:ss.milliseconds]
