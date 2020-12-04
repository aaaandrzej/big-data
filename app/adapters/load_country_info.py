import csv


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


def cc_decoder(file, fieldnames=CC_FIELDNAMES):
    with open(file) as csv_file:
        for i in range(50):
            csv_file.__next__()
        reader = csv.DictReader(csv_file, delimiter='	', fieldnames=fieldnames)
        cc_decoded = {row['ISO']: row['Country'] for row in reader}
        return cc_decoded


def capital_finder(file, fieldnames=CC_FIELDNAMES):
    with open(file) as csv_file:
        for i in range(50):
            csv_file.__next__()
        reader = csv.DictReader(csv_file, delimiter='	', fieldnames=fieldnames)
        capitals = {row['Country']: row['Capital'] for row in reader}
        return capitals
