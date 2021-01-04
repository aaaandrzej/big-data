from decimal import Decimal

import boto3

from app.config import ENDPOINT_URL


def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=ENDPOINT_URL)

    table = dynamodb.create_table(
        TableName='AirportFinderTable',
        KeySchema=[
            {
                'AttributeName': 'geonameid',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'name',
                'KeyType': 'RANGE',  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'geonameid',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'name',
                'AttributeType': 'S',
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


def save_item_to_dynamodb(item, table_name='AirportFinderTable', output_fieldnames=None, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=ENDPOINT_URL)

    table = dynamodb.Table(table_name)

    if table_name not in [t.name for t in dynamodb.tables.all()]:  # TODO optimize this check
        print(f'table not found, creating {table_name}')
        create_table()

    if output_fieldnames:
        print(item)
        item = {k: item[k] for k in output_fieldnames if k in item}
        print(item)

    item['longitude'] = Decimal(str(item['longitude']))  # TODO DDB error workaround, refactor probably required
    item['latitude'] = Decimal(str(item['latitude']))

    table.put_item(Item=item)
    print(item)
    print()


def save_df_to_dynamodb(df, table_name='AirportFinderTable', output_fieldnames=None, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=ENDPOINT_URL)

    for item in df.to_dict(orient="records"):
        save_item_to_dynamodb(item, table_name=table_name, output_fieldnames=output_fieldnames, dynamodb=dynamodb)


if __name__ == '__main__':
    # new_table = create_table()
    # print("Table status:", new_table.table_status)
    # load_movies(movie_list)
    # database = boto3.resource('dynamodb', endpoint_url=ENDPOINT_URL)
    #
    #     print('table exists')

    pass
