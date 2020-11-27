import csv
from dataclasses import dataclass
from datetime import datetime
import os


@dataclass
class SalesRecord:
    region: str
    country: str
    item_type: str


def timer(func):
    def wraps():
        start = datetime.now()
        func()
        finish = datetime.now()
        print(f'execution time: {finish - start} [h:mm:ss.milliseconds]')
        return

    return wraps


directory = ''
file = 'data_sample.csv'


@timer
def print_csv_rows_converted_to_objects(directory=directory, file=file):
    counter = 0
    with open(os.path.join(directory, file), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # skipping the header row
        for row in reader:
            region, country, item_type, *remaining = row
            sales_record = SalesRecord(region, country, item_type)
            print(sales_record)
            counter += 1
            if counter >= 1000:
                break
    stats = f'\n{counter} lines printed\n'
    print(stats)
    return


print_csv_rows_converted_to_objects()
